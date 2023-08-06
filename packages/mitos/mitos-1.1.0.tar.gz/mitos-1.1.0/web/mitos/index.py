'''
@author: M. Bernt
'''
import glob
import json
import os
import random
import re
import string
import subprocess
import sys
import traceback
from io import StringIO

import mod_python
from Bio import SeqIO
from Bio.Alphabet.IUPAC import ambiguous_dna
from Bio.SeqRecord import SeqRecord

import mitos
from mitos import (
    CONFIG,
    draw,
    webserver,
)
from mitos.mitofile import mitofromfile
from mitos.sequence import (
    AlphabetException,
    MultiFastaException,
    NoFastaException,
    sequence_info_fromfile,
    sequence_info_fromfilehandle,
    sequences_fromfile,
)


class MITOSHashEmpty(Exception):
    """
    Exception when no hash was given
    """
    def __str__(self):
        """
        print exception
        """
        return "no job ID specified. "


class MITOSHashInvalid(Exception):
    """
    Exception when no hash was given
    """
    def __init__(self, hsh, req):
        self._hsh = hsh
        req.log_error("access to non existent hash {hsh} ".format(hsh=hsh), mod_python.apache.APLOG_ALERT)

    def __str__(self):
        """
        print exception
        """
        return "the requested ID ({hsh}) is invalid.".format(hsh=self._hsh)


class MITOSMaxSizeException(Exception):
    """
    Exception to be raised when a to large sequence is found
    """
    def __str__(self):
        """
        print exception
        """
        return "sequence to large"


class MITOSMinSizeException(Exception):
    """
    Exception to be raised when a to small sequence is found
    """
    def __str__(self):
        """
        print exception
        """
        return "sequence to small"


class EmptySequenceException(Exception):
    """
    Exception to be raised when an empty sequence is found
    """
    def __str__(self):
        """
        print exception
        """
        return "Sequence empty"


class LargeFastaException(Exception):
    """
    Exception to be raised when to many sequences are in the fasta file
    """
    def __str__(self):
        """
        print exception
        """
        return "to many sequences are in the fasta file"


class JSONSaveException(Exception):
    """
    Exception when job file was save incomplete
    """
    def __str__(self):
        """
        print excption
        """
        return "Could not save JSON file"


def formvalueinput(s):
    """
    try to parse unicode form values
    """
    enc = ["utf8", "cp1252", "latin-1"]
    for e in enc:
        try:
            s = s.decode(e)
        except UnicodeDecodeError:
            continue
        else:
            break
    return s


def gen_hash(length):
    """
    generate a hash of digits and (lower and upper case) letters of a given length
    the first character must be a letter
    @param length the desired length
    @return the hash
    """
    fst = string.ascii_uppercase + string.ascii_lowercase
    cha = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join([random.choice(fst)] + [random.choice(cha) for _ in range(length - 1)])


def getfirst_unicode(form, var, absent=None):
    '''
       A utf8/cp1252-decoding version of form.getfirst().
       Almost all cp1252 is invalid as utf8, so cp1252 is the fallback.
       If var is not in the form, it returns the absent value
       (By default this is None. It may be convenient to use u'' or even 0)
       see http://helpful.knobs-dials.com/index.php/Mod_python_notes#mod_python_and_Unicode
    '''
    s = form.getfirst(var)
    if s is None:
        return absent
    s = formvalueinput(s)
    return s


def gethash(req):
    """
    get the hash from the request
    @return None iff hash is invalid or job crashed, otherwise the hash
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = getfirst_unicode(form, "hash")
#     hsh = form.getfirst("hash")
    # for compatibility with old links: if hsh is not in the hsh field of the
    # request then consider everything as hsh
    if hsh is None:
        hsh = req.args
    try:
        if hsh is None or len(hsh) == 0:
            raise MITOSHashEmpty
        if hsh[-1] == "/":
            hsh = hsh[:-1]
        # no job, log, or wrk file -> invalid hsh
        if len(glob.glob("%s/%s.*" % (CONFIG.TOMCATPATH, hsh))) == 0:
            raise MITOSHashInvalid(hsh, req)
    except (MITOSHashInvalid, MITOSHashEmpty) as e:
        inhalt = """Sorry, {error}<br>
<br>
If you were directed to this page via the link in the MITOS result email
check if the line is broken across multiple lines. <br>
You can try to paste the link of the form
http://{url}result.py?hash=HASH directly to the browser, where HASH consists of 8 characters or numbers.
<br>
<br>
If the problem persists please contact us!""".format(error=str(e), url=CONFIG.WEBPATH)
        req.write(webserver.makeMitos(inhalt, 2, titlesfx="Results"))
        return None
    return hsh


def getjob(req, hsh):
    """
    get the job file for the hash
    @return the job if it is finished, otherwise None
    """
    # job is still in work
    if os.path.exists("%s/%s.job" % (CONFIG.TOMCATPATH, hsh)) or \
       os.path.exists("%s/%s.wrk" % (CONFIG.TOMCATPATH, hsh)):
        queued = glob.glob(CONFIG.TOMCATPATH + "/*.job")
        # sort the job files by date. since the server might alter this list
        # the getmtime foo might cause an OSError thus this little bit
        # complicated while loop - try except construction
        while True:
            try:
                queued.sort(key=lambda x: os.path.getmtime(x))
            except OSError:
                queued = glob.glob(CONFIG.TOMCATPATH + "/*.job")
                continue
            else:
                break
        try:
            pos = queued.index(CONFIG.TOMCATPATH + hsh + ".job")
        except ValueError:
            pos = -1
        if pos < 0:
            inhalt = "Your sequence (job: {hsh}) is currently being analyzed".format(hsh=hsh)
        else:
            inhalt = """Your job ({hsh}) is on position {pos} in the queue.<br>
<a href=\"modify.py?hash={hsh}&from=job\">Click here to DELETE your job!</a><br>
""".format(pos=pos + 1, hsh=hsh)
        f = open("%swait.txt" % (CONFIG.MITOSPATH))
        inhalt += f.read()
        f.close()
        req.write(webserver.makeMitos(inhalt, 2, titlesfx="Results"))
        return None
    # job finished
    elif os.path.exists("%s/%s.log" % (CONFIG.TOMCATPATH, hsh)):
        f = open("%s/%s.log" % (CONFIG.TOMCATPATH, hsh), "r")
        job = json.load(f)
        f.close()
        inhalt = ""
        # but no results directory (deleted)
        if not os.path.exists("%s/%s/" % (CONFIG.TOMCATPATH, hsh)):
            inhalt = """Sorry, the results for the job with ID {hsh} are not available anymore<br>
(due to space limitation we need to remove results after a few months).""".format(hsh=hsh)
            if "fastacontent" in job:
                inhalt += """<br><br> You may restart the job by clicking <a href="modify.py?hash={hsh}&from=log">here</a>.""".format(hsh=hsh)
        elif not os.path.exists("%s/%s/result" % (CONFIG.TOMCATPATH, hsh)):
            inhalt = "Sorry, the job with ID {hsh} has crashed.<br>Please contact us!".format(hsh=hsh)
        if inhalt != "":
            req.write(webserver.makeMitos(inhalt, 2, titlesfx="Results"))
            return None
    # Not a job, log, or wrk file?
    else:
        inhalt = "Sorry, a job with ID {hsh} could not be found.<br>Please contact us!".format(hsh=hsh)
        req.write(webserver.makeMitos(inhalt, 2, titlesfx="Results"))
        return None
    return job


def filehandle(req):
    """
    code for getting a file
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = gethash(req)
    if hsh is None:
        return
    # try to get the job file (even if the job data is not used the function
    # ensures that the results - and thereby the file - are there)
    job = getjob(req, hsh)
    if job is None:
        return
#     name = form.getfirst("name")
    name = getfirst_unicode(form, "name")
#     outputtype = form.getfirst("type")
    outputtype = getfirst_unicode(form, "type")
    if hsh[-1] == "/":
        hsh = hsh[:-1]
#    # determine the output type from the file name extension
#    outputtype = os.path.splitext(req.filename)[1][1:]
    # read the results
    mito = mitofromfile("%s/%s/result" % (CONFIG.TOMCATPATH, hsh))
    featurelist = mito.getfeatures()
    acc = mito.accession
    # generate the output
    if outputtype == "zip":
        if not os.path.exists("{path}/{hash}.zip".format(path=CONFIG.TOMCATPATH, hash=hsh)):
            ret = subprocess.call("cd {path}; zip -9 -y -r {hash}.zip  {hash}/".format(path=CONFIG.WRKPATH, hash=hsh), shell=True)
            if ret != 0:
                raise Exception("Could not create zip for {hash} return code was {retcode}".format(hash=hsh, retcode=ret))
            os.chmod("{path}/{hash}.zip".format(path=CONFIG.TOMCATPATH, hash=hsh), 0o0777)
        req.content_type = 'application/octet-stream'
        req.headers_out["Content-Disposition"] = "attachment; filename={name}.{type}".format(name=name, type=outputtype)
        file = open("{path}/{hash}.zip".format(path=CONFIG.TOMCATPATH, hash=hsh))
        for line in file.readlines():
            req.write(line)
        file.close()
    elif outputtype == "fas" or outputtype == "faa":
        req.content_type = 'text/plain'
        req.headers_out["Content-Disposition"] = "attachment; filename={name}.{type}".format(name=name, type=outputtype)
        sequence = sequences_fromfile("%s/%s/sequence.fas" % (CONFIG.TOMCATPATH, hsh), circular=True)[0]
        webserver.genoutput(featurelist, acc, outputtype, req, sequence, job["code"])
    else:
        req.content_type = 'text/plain'
        req.headers_out["Content-Disposition"] = "attachment; filename={name}.{type}".format(name=name, type=outputtype)
        webserver.genoutput(featurelist, acc, outputtype, req)


def handler(req):
    req.content_type = 'text/html'
    reqfile = os.path.basename(req.filename)
    if CONFIG.MAINTENANCE:
        maintenance(req)
    elif reqfile == 'help.py':
        helphandle(req)
    elif reqfile == 'history.py':
        historyhandle(req)
    # upload the sequence and generate job entry
    elif reqfile == 'upload.py':
        uploadhandle(req)
    elif reqfile == "modify.py":
        modifyhandle(req)
    elif reqfile == "result.py":
        resulthandle(req)
    elif reqfile.startswith("rnaplot"):
        rnaplot(req)
    elif reqfile == "plot.py":
        plot(req)
    elif reqfile == "download.py":
        filehandle(req)
    elif reqfile == "picture.py":
        pichandle(req)
    elif reqfile == "settings.py":
        settingshandle(req)
    elif reqfile == "stats.py":
        stathandle(req)
#    elif reqfile == "bigpic.jpg":
#        bigpichandle(req)
#    elif reqfile == 'index2.py':
#        index2handle(req)
    # start page
    else:
        index2handle(req)
    return mod_python.apache.OK


def helphandle(req):
    """
    generate the help page
    """
    f = open("%shelp.txt" % (CONFIG.MITOSPATH))
    helptxt = f.read().format(mail=CONFIG.MITOS_CONTACTMAILCRYPT, mitosurl=CONFIG.WEBPATH)
    req.write(webserver.makeMitos(helptxt, 0, titlesfx="Help"))
    f.close()


def historyhandle(req):
    """
    generate the history page
    """
    f = open("%shistory.txt" % (CONFIG.MITOSPATH))
    hst = ""
    for line in f.readlines():
        line = line.split("|")
        hst += "<dt>%s</dt>\n" % (line[0])
        hst += "<dd><ul>\n"
        for i in range(1, len(line)):
            hst += "<li>%s</li>\n" % (line[i])
        hst += "</ul></dd>\n"
    f.close()
    content = """<div style="width:680px;margin:0 auto;text-align:justify;" >
    All changes of the MITOS algorithm or changes to the website that
influence the outcome of MITOS are listed here. Changes solely to the
website are not listed.
    <br><br>
If you want to include the revision number while citing MITOS you can
safely use the latest listed below.
    <dl>
    {hist}
    </dl>
    </div>""".format(hist=hst)
    req.write(webserver.makeMitos(content, 0, titlesfx="History"))


def htmlsave(s):
    """
    return a (well not perfectly) html save copy of the string
    @param s a string
    @return recoded string
    """
    s = s.encode('ascii', 'xmlcharrefreplace')
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
#     s = s.replace("&", "&amp;") & is replaced by encode
    s = s.replace("'", "&#39;")
    s = s.replace("\"", "&quot;")
    return s


def index2handle(req):
    f = open("%sindex.txt" % (CONFIG.MITOSPATH))
    content = f.read()
    # + "<script> $('.hidein').attr('style','display: table-row');</script>"
    f.close()
    f = open("%snews.txt" % (CONFIG.MITOSPATH))
    news = f.read()
    f.close()
    req.write(webserver.makeMitos(content, 1, news=news))


def maintenance(req):
    content = "The MITOS webserver is under maintenance. We expect to be back online: {date}".format(date=CONFIG.MAINTENANCE)
    req.write(webserver.makeMitos(content, 1, titlesfx="Maintenance"))


def modifyhandle(req):
    """
    code to remove/restart a job
    - job -> log (delete)
    - log -> job (restart)
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = gethash(req)
    if hsh is None:
        return
#     fm = form.getfirst("from")
    fm = getfirst_unicode(form, "from")
#    f = open("%s/.lock" % (CONFIG.WRKPATH), "w")
#    os.chmod("%s/.lock" % (CONFIG.WRKPATH), 0775)
#    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    to = None
    if fm == "job" and os.path.exists(CONFIG.TOMCATPATH + "/" + hsh + ".job"):
        to = "log"
    elif fm == "log" and os.path.exists(CONFIG.TOMCATPATH + "/" + hsh + ".log"):
        to = "job"
    if to is not None:
        try:
            os.rename("%s/%s.%s" % (CONFIG.TOMCATPATH, hsh, fm), "%s/%s.%s" % (CONFIG.TOMCATPATH, hsh, to))
        except OSError:  # if failed -> check if the job was renamed to wrk or even log already
            if os.path.exists(CONFIG.TOMCATPATH + "/" + hsh + ".wrk") or os.path.exists(CONFIG.TOMCATPATH + "/" + hsh + ".job"):
                to = None  # reset to to none to indicate an error
            else:
                raise
        else:
            if to == "job":
                req.write('<script type="text/javascript">location.replace("./result.py?hash={hsh}");</script>'.format(hsh=hsh))
            else:
                req.write('<script type="text/javascript">location.replace("./index.py");</script>')
    # else
    if to is None:
        if fm == "job":
            txt = "<b>Could not cancel your job.</b> It seems to be running already.<br>\n"
        else:
            txt = "<b>Could not restart your job.</b> Please contact us.\n"
        txt += '<script type="text/javascript">window.setTimeout("location.replace(\\"result.py?hash=%s\\")", 3600);</script>' % (hsh)
        f = open("%swait.txt" % (CONFIG.MITOSPATH))
        req.write(webserver.makeMitos(txt + f.read(), 1, titlesfx="Break"))
        f.close()


def pichandle(req):
    """
    render a small picture of the annotation
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = gethash(req)
    if hsh is None:
        return
    # try to get the job file (even if the job data is not used the function
    # ensures that the results - and thereby the picture - are there)
    job = getjob(req, hsh)
    if job is None:
        return
#     name = form.getfirst("name")
    name = getfirst_unicode(form, "name")
#     size = form.getfirst("size")
    size = getfirst_unicode(form, "size")
    if hsh[-1] == "/":
        hsh = hsh[:-1]
    mito = mitofromfile("%s/%s/result" % (CONFIG.TOMCATPATH, hsh))
    sequence = sequences_fromfile("%s/%s/sequence.fas" % (CONFIG.TOMCATPATH, hsh), circular=False)[0]
    if size == "small":
        img = draw.draw2(mito.getfeatures(), len(sequence))
    elif size == "big":
        img = draw.draw3(mito.getfeatures(), len(sequence))
    else:
        raise Exception("Unknown image size: {size}\n{form}".format(size=size, form=str(form)))
    req.content_type = 'image/*'
    req.headers_out["Content-Disposition"] = "attachment; filename={name}.png".format(name=name)
    req.write(img)


def plot(req):
    """
    get the plots fot RNA or protein '
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = gethash(req)
    if hsh is None:
        return
    job = getjob(req, hsh)
    if job is None:
        return
    name = getfirst_unicode(form, "name")
    type = getfirst_unicode(form, "type")
    if type != "rna" and type != "prot":
        found = "Invalid plot type requested. Please contact us.<br>\n"
        found += '<script type="text/javascript">window.setTimeout("location.replace(\\"./result.py?hash=%s/\\")", 5000);</script>' % (hsh)
        req.write(webserver.makeMitos(found, 1))
        return mod_python.apache.OK
    if os.path.exists("{webpath}/{hsh}/plots/{type}.pdf".format(hsh=hsh, webpath=CONFIG.TOMCATPATH, type=type)):
        req.content_type = 'application/pdf'
        req.headers_out["Content-type"] = "application/force-download"
        req.headers_out["Content-Disposition"] = "attachment; filename={name}.pdf".format(name=name)
        req.sendfile("{webpath}/{hsh}/plots/{type}.pdf".format(hsh=hsh, webpath=CONFIG.TOMCATPATH, type=type))
    else:
        if type == "prot":
            found = "No BLAST hits were reported for this sequence.  <br>\n"
        elif type == "rna":
            found = "No RNA plot was found. <br>\n"
            if job["trna"] or job["rrna"]:
                found += "<br>Your job was computed prior to the introduction of this feature. <br>\n"
                found += "The plot can be generated by restarting your job.<br>"
                found += """You may restart the job by clicking <a href="modify.py?hash={hsh}&from=log">here</a>.""".format(hsh=hsh)
        found += """<div style="float:left; text-align: left; "><a href="result.py?hash={hsh}">Back</a><br>\n</div>
        <script type="text/javascript">window.setTimeout("location.replace(\\"./result.py?hash={hsh}/\\")", 6000);</script>
        """.format(hsh=hsh)
        req.write(webserver.makeMitos(found, 1))
    return mod_python.apache.OK


def resulthandle(req):
    """
    get the results
    """
    hsh = gethash(req)
    if hsh is None:
        return
    job = getjob(req, hsh)
    if job is None:
        return
    mito = mitofromfile("%s/%s/result" % (CONFIG.TOMCATPATH, hsh))
    seq = sequence_info_fromfile("%s/%s/sequence.fas" % (CONFIG.TOMCATPATH, hsh), alphabet=ambiguous_dna, circular=False)
    fastahead = seq[0]["name"]
    fnm = ''.join(ch for ch in mito.accession if ch.isalnum())
    # get the html formatted result table and file links
    inhalt = """<div style="float:left; text-align: left; ">
Downloads:<br>
<a href="download.py?type=bed&name={name}&hash={hsh}">BED file</a><br>\n
<a href="download.py?type=gff&name={name}&hash={hsh}">GFF file</a><br>\n
<a href="download.py?type=tbl&name={name}&hash={hsh}">TBL file</a><br>
<a href="download.py?type=txt&name={name}&hash={hsh}">Gene Order file</a><br>
<a href="download.py?type=fas&name={name}&hash={hsh}">FAS file</a><br>
<a href="download.py?type=faa&name={name}&hash={hsh}">FAA file</a><br>
<br>
Raw data:<br>
<a href="plot.py?name={name}&hash={hsh}&type=prot">protein plot</a><br>
<a href="plot.py?name={name}&hash={hsh}&type=rna">ncRNA plot</a><br>
<a href="download.py?type=zip&name={name}&hash={hsh}">raw data</a><br>
<br>
Misc:<br>
<a href="settings.py?hash={hsh}">Job settings</a><br>
</div>""".format(hsh=hsh, name=fnm)
    if "jobid" in job and job["jobid"] != "":
        jid = job["jobid"]
    else:
        jid = job["filename"]
    inhalt += """<div style="width:500px;margin:0 auto;">
<b>Jobid: {jobid} ({fastahead})</b><br><br>
<table border="0" cellspacing="0" cellpadding ="0" style="margin:auto;">
<tr>
    <td class="ftd"><b>Name</b></td>
    <td class="ftd"><b>Start</b></td>
    <td class="ftd"><b>Stop</b></td>
    <td class="ftd"><b>Strand</b></td>
    <td class="ftd"><b>Length</b></td>
    <td class="ftd"><b>Structure</b></td>
</tr>
""".format(jobid=jid.encode('utf-8'), fastahead=fastahead)
    featurelist = mito.getfeatures()
    for feature in featurelist:
        if feature.type == "tRNA" or feature.type == "rRNA":
            links = """<a href="rnaplot.py?hash={hsh}&fname={fname}&name={name}&start={start}&stop={stop}&type=svg">svg</a> <a href="rnaplot.py?hash={hsh}&fname={fname}&name={name}&start={start}&stop={stop}&type=ps">ps</a>""".format(hsh=hsh, start=feature.start, stop=feature.stop, name=fnm, fname=feature.name)
        else:
            links = ""
        inhalt += """
<tr>
    <td class=\"ftd\">{name}</td>
    <td class=\"ftd\">{start:d}</td>
    <td class=\"ftd\">{stop}</td>
    <td class=\"ftd\">{pm}</td>
    <td class=\"ftd\">{length}</td>
    <td class=\"ftd\">{links}</td>
</tr>""".format(name=feature.getname(), start=feature.start + 1,
                stop=feature.stop + 1, pm=feature.plusminus(),
                length=feature.stop - feature.start + 1, links=links)
    if job["trna"]:
        trnaind = '<td><div style=\"background-color:blue;height:10px;width: 10px\" ></div></td><td>tRNA gene</td>'
    else:
        trnaind = '<td></td><td></td>'
    if job["rrna"]:
        rrnaind = '<td><div style=\"background-color:green;height:10px;width: 10px\" ></div></td><td>rRNA gene</td>'
    else:
        rrnaind = '<td></td><td></td>'
    if job["prot"]:
        protind = '<td><div style=\"background-color:red;height:10px;width: 10px\" ></div></td><td>protein coding gene</td>'
    else:
        protind = '<td></td><td></td>'
    inhalt += """</table>
</div>
<table style=\"margin:auto\">
<tr>
{trnaind}
{rrnaind}
{protind}
</tr>
</table>
<a href=\"picture.py?name={name}&hash={hsh}&size=big\"><img src = \"picture.py?name={name}&hash={hsh}&size=small\" width=\"700\"></img></a>
""".format(hsh=hsh, name=fnm, trnaind=trnaind, rrnaind=rrnaind, protind=protind)
    mis, dup, nst = mitos.problems(job["prot"], job["trna"], job["rrna"], False, featurelist)
    if len(mis) + len(dup) + len(nst) > 0:
        inhalt += "<br> <br> <div>Warning(s) and peculiarities:<br>  <ul style=\"text-align: left;display:-moz-inline-stack;display:inline-block;zoom:1;*display:inline;\">"
    if len(mis) > 0:
        inhalt += "<li>Genes not found: %s </li>" % (", ".join(mis))
    if len(dup) > 0:
        inhalt += "<li>Split/duplicated genes: %s </li>" % (", ".join(dup))
    if len(nst) > 0:
        inhalt += "<li>Non standard features: %s </li>" % (", ".join(nst))
    if len(mis) + len(dup) + len(nst) > 0:
        inhalt += "</ul><br>Tip(s):<br><ul style=\"text-align: left;display:-moz-inline-stack;display:inline-block;zoom:1;*display:inline;\"> "
        if len(mis) > 0:
            inhalt += "<li>Consult the protein and ncRNA plots if there is a signal <br> for the genes that MITOS could not determine automatically.</li>"
        if len(dup) > 0:
            inhalt += "<li>Check the quality/e-values of the predictions for evaluating their reliability.</li>"
        inhalt += "</ul></div>"
    # render the result page
    req.write(webserver.makeMitos(inhalt, 2, titlesfx="Results"))


def rnaplot(req):
    """
    get the structure plot for an RNA
    request specifies start, stop, name (of the sequenc), fname (name of the feature),
    and type (svg / ps)
    """
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    hsh = gethash(req)
    if hsh is None:
        return
    # try to get the job file (even if the job data is not used the function
    # ensures that the results - and thereby the RNA plot - are there)
    job = getjob(req, hsh)
    if job is None:
        return
    start = int(form.get("start", None))
    stop = int(form.get("stop", None))
    name = str(form.get("name", None))
    fname = str(form.get("fname", None))
    type = str(form.get("type", None))
    if type != "svg":
        req.content_type = 'application/postscript'
    req.headers_out["Content-Disposition"] = "attachment; filename={name}-{fname}-{start}-{stop}.{type}".format(name=name, fname=fname, start=start, stop=stop, type=type)
    fl = glob.glob("%s/plots/*-%d-%d.%s" % (CONFIG.TOMCATPATH + hsh, start, stop, type))
    # FOR COMAPTIBILITY TO OLD ACCESS PATHS (SAVE TO DELETE AFTER 12 AUG. 2012)
    fl += glob.glob("%s/rna/*-%d-%d.%s" % (CONFIG.TOMCATPATH + hsh, start, stop, type))
    if len(fl) == 0:
        raise Exception("%s: no plot at position %d %d" % (hsh, start, stop))
    if len(fl) > 1:
        raise Exception("%s: more than one plot at position %d %d" % (hsh, start, stop))
    req.sendfile(fl[0])


def settingshandle(req):
    """
    print job settings
    """
    hsh = gethash(req)
    if hsh is None:
        return
    job = getjob(req, hsh)
    if job is None:
        return
    inhalt = """
<div style="float:left; text-align: left; ">
<a href="result.py?hash={hsh}">Back</a><br>\n
</div>""".format(hsh=hsh)
    if "jobid" in job and job["jobid"] != "":
        inhalt += "<h3>Job ID: {id}</h3>".format(id=htmlsave(job["jobid"]))
    else:
        job["filename"] = job["filename"].encode('ascii', 'xmlcharrefreplace')
        inhalt += "<h3>Job for file: {filename}</h3>".format(filename=htmlsave(job["filename"]))
    inhalt += """<table border="0" cellspacing="0" style="margin:auto;white-space:nowrap;">
<tr>
    <th class="std"><b>Property</b></th>
    <th class="std"><b>Value</b></th>
</tr>
<tr>
    <td class=\"std\">Genetic Code</td><td class=\"std\">{code}</td>
</tr>
<tr>
    <td class=\"std\">Proteins</td><td class=\"std\">{prot}</td>
</tr>
<tr>
    <td class=\"std\">tRNAs</td><td class=\"std\">{trna}</td>
</tr>
<tr>
    <td class=\"std\">rRNAs</td><td class=\"std\">{rrna}</td>
</tr>
<tr>
    <td class=\"std\">BLAST E-value Exponent</td><td class=\"std\">{evalue}</td>
</tr>
<tr>
    <td class=\"std\">Cutoff</td><td class=\"std\">{cutoff}%</td>
</tr>
<tr>
    <td class=\"std\">Maximum Overlap</td><td class=\"std\">{maxovl}%</td>
</tr>
<tr>
    <td class=\"std\">Clipping Factor</td><td class=\"std\">{clipfac}</td>
</tr>
<tr>
    <td class=\"std\">Fragment Overlap</td><td class=\"std\">{fragovl}%</td>
</tr>
<tr>
    <td class=\"std\">Fragment Quality Factor</td><td class=\"std\">{fragfac}</td>
</tr>
<tr>
    <td class=\"std\">Start/Stop Range</td><td class=\"std\">{ststrange} aa</td>
</tr>
<tr>
    <td class=\"std\">Final Maximum Overlap</td><td class=\"std\">{finovl} nt</td>
</tr>
""".format(code=job["code"], prot=job["prot"], trna=job["trna"], rrna=job["rrna"],
           cutoff=job["cutoff"], evalue=job["evalue"], clipfac=job["clipfac"],
           ststrange=job["ststrange"], finovl=job["finovl"], fragfac=job["fragfac"],
           fragovl=job["fragovl"] * 100, maxovl=job["maxovl"] * 100)
    inhalt += """
    </table>
    """
    # render the result page
    req.write(webserver.makeMitos(inhalt, 2, titlesfx="Settings"))


def stathandle(req):
    """
    print statistics
    """
    if os.path.exists('{ldir}/stats.json'.format(ldir=CONFIG.WRKPATH)):
        with open('{ldir}/stats.json'.format(ldir=CONFIG.WRKPATH), 'r') as fp:
            stats = json.load(fp)
        inhalt = """
        <h2>Status</h2>
        {queued} Job(s) are queued or processed. <br>
        <h2>Statistics</h2>
        MITOS has processed<br><br>
        {jobs} jobs<br><br>
        {seqlen} nt<br><br>
        ({jobs_day} / {jobs_week} / {jobs_month} jobs in the last day / week / month)<br><br>
        Last update: {date}
        """.format(**stats)
    else:
        inhalt = """<h2>Status</h2>Status information could not be loaded."""
    req.write(webserver.makeMitos(inhalt, 2, titlesfx="Status & Statistics"))


def uploadhandle(req):
    f = open("%supload.txt" % (CONFIG.MITOSPATH))
    uptxt = f.read()
    req.write(webserver.makeMitos(uptxt.format(email=CONFIG.MITOS_CONTACTMAIL, mitosurl=CONFIG.WEBPATH), 1, titlesfx="Upload"))
    f.close()
    # render the text informing the user that the file is uploaded
    req.write('<script type="text/javascript">document.getElementById("Begin").style.display = "block";</script>\n')
#     formdata = mod_python.util.FieldStorage(req)
    form = mod_python.util.FieldStorage(req, keep_blank_values=1)
    conf = {}
    try:
        conf["name"] = getfirst_unicode(form, "name").strip()
        conf["email"] = getfirst_unicode(form, "email").strip()
        conf["code"] = int(getfirst_unicode(form, "code"))
        conf["jobid"] = getfirst_unicode(form, "jobid").strip()
        conf["cutoff"] = int(round(float(getfirst_unicode(form, "cutoff"))))
        conf["clipfac"] = float(getfirst_unicode(form, "clipfac"))
        conf["evalue"] = float(getfirst_unicode(form, "evalue"))
        conf["ststrange"] = int(getfirst_unicode(form, "ststrange"))
        conf["finovl"] = int(round(float(getfirst_unicode(form, "finovl"))))
        conf["fragovl"] = float(getfirst_unicode(form, "fragovl")) / 100.0
        conf["fragfac"] = float(getfirst_unicode(form, "fragfac"))
        conf["maxovl"] = float(getfirst_unicode(form, "maxovl")) / 100.0
        conf["prot"] = "prot" in form
        conf["trna"] = "trna" in form
        conf["rrna"] = "rrna" in form
        multi = "multi" in form
        conf["filename"] = formvalueinput(form["myFile"].filename)
    except (KeyError, ValueError):
        req.write('<script type="text/javascript">document.getElementById("invalidform").style.display = "block";</script>\n')
        return
    except Exception:
        req.log_error("Request could not be handled: %s " % (str(form)), mod_python.apache.APLOG_ALERT)
        req.write('<script type="text/javascript">document.getElementById("internal").style.display = "block";</script>\n')
        return
#     if 1:
    try:
        # read sequence from fasta file and check:
        # - if it is a fasta file (ie if the fasta parser was able to read a sequence)
        # - if only one sequence was submitted
        # - if the sequence is not empty
        # - if it is not too long (for RNA search)
        # - if it has a name (if not set 'NoName')
        fasta = formvalueinput(form["myFile"].value)
        fasta = fasta.encode('ascii', 'ignore')
        fh = StringIO(fasta)
        sequences = sequence_info_fromfilehandle(fh, alphabet=ambiguous_dna, circular=False)
        fh.close()
        if len(sequences) == 0:
            raise NoFastaException
        if not multi and len(sequences) > 1:
            raise MultiFastaException
        if len(sequences) > CONFIG.MITOS_MAXNRSEQ:
            raise LargeFastaException
        for si in range(len(sequences)):
            if len(sequences[si]["sequence"]) == 0:
                raise EmptySequenceException
            if len(sequences[si]["sequence"]) <= CONFIG.MITOS_MINSEQSIZE:
                raise MITOSMinSizeException
            if (conf["rrna"] or conf["trna"]) and (len(sequences[si]["sequence"]) > CONFIG.MITOS_MAXSEQSIZE):
                raise MITOSMaxSizeException
            if sequences[si]["description"] == "":
                sequences[si]["description"] = "NoName"
            sequences[si]["id"] = re.sub('[|\t]', '_', sequences[si]["id"])
            sequences[si]["name"] = re.sub('[|\t]', '_', sequences[si]["name"])
            sequences[si]["description"] = re.sub('[|\t]', '_', sequences[si]["description"])
            # determine a hash for the dirname
            # create the directory
            # write the sequence into sequence.fas in the directory
            # make sure that no such dir exists already
    #         m = hashlib.sha256()
    #     #        m.update(name + email + filename + ctime())
    #         m.update(conf["name"] + conf["email"] + formdata["myFile"].value + ctime())
    #         conf["hash"] = m.hexdigest()
            ncol = 0
            while True:
                conf["hsh"] = gen_hash(8)
#                 m = hashlib.sha256()
#                 m.update(conf["name"].encode('utf8', 'replace'))
#                 m.update(str(conf["email"]))
#                 m.update(fasta.encode('utf8', 'replace'))
#                 m.update(time.ctime())
#                 m.update(str(random.random()))
#                 x = base64.urlsafe_b64encode(m.hexdigest())
#                 # remove non alpha-numerical characters
#                 x = re.sub('[\W_]+', '', x)
#                 # get CONFIG.MITOS_HASHLEN random digits from the remaining
#                 conf["hsh"] = ''.join(random.sample(x, len(x)))[:8]
                if len(glob.glob("%s/%s*" % (CONFIG.TOMCATPATH, conf["hsh"]))) == 0:
                    break
                else:
                    ncol += 1
            # report an alert if there was one or more collissions
            if ncol > 0:
                req.log_error("hash created after {ncol} collissions ".format(ncol=ncol), mod_python.apache.APLOG_ALERT)
            # write fasta file to conf[]
            # this is done through SeqIO to ensure a properly and consistent formatted fasta file
            # in particular this ensures that the sequences are upper case
            sr = SeqRecord(seq=sequences[si]["sequence"], id=sequences[si]["id"],
                           name=sequences[si]["name"], description=sequences[si]["description"])
            f = StringIO()
            SeqIO.write(sr, f, "fasta")
            fasta = f.getvalue()
            f.close()
            # encode as ascii for the fasta content .. stripping all foreign characters
            conf["fastacontent"] = fasta.encode('ascii', 'ignore')
            conf["seqlen"] = len(sequences[si]["sequence"])
            if conf["jobid"] == "":
                conf["jobid"] = sequences[si]["description"]
            # write job file
            try:
                f = open("%s/%s.job" % (CONFIG.TOMCATPATH, conf["hsh"]), "w")
                json.dump(conf, f, indent=3, sort_keys=True)
                f.close()
            except Exception:
                stream = StringIO()
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=stream)
                req.log_error("""could not dump json file for {job}
    # exception was: {exc}
    # content was {content}
    # """.format(job=conf["hsh"], content=str(conf), exc=stream.getvalue()), mod_python.apache.APLOG_ALERT)
                raise JSONSaveException
            os.chmod("%s/%s.job" % (CONFIG.TOMCATPATH, conf["hsh"]), 0o0777)
            # temporary code to find nasty unicode error .. just reloads the json file to see if writing worked
            try:
                f = open("%s/%s.job" % (CONFIG.TOMCATPATH, conf["hsh"]))
                json.load(f)
                f.close()
            except Exception:
                stream = StringIO()
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=stream)
                req.log_error("""could not reload json file for {job}
    exception was: {exc}
    content was {content}
    """.format(job=conf["hsh"], content=str(conf), exc=stream.getvalue()), mod_python.apache.APLOG_ALERT)
                raise JSONSaveException
        req.write('<script type="text/javascript">document.getElementById("Finish").style.display = "block";</script>\n')
        # after some waiting replace with wait.py
        req.write('<script type="text/javascript">window.setTimeout("location.replace(\\"result.py?hash=%s\\")", 5000);</script>\n' % (conf["hsh"]))
    except JSONSaveException:
        req.write('<script type="text/javascript">document.getElementById("internal").style.display = "block";</script>\n')
    except EmptySequenceException:
        req.write('<script type="text/javascript">document.getElementById("empty").style.display = "block";</script>\n')
    except MITOSMaxSizeException:
        req.write('<script type="text/javascript">document.getElementById("maxsize").style.display = "block";</script>\n')
    except MITOSMinSizeException:
        req.write('<script type="text/javascript">document.getElementById("minsize").style.display = "block";</script>\n')
    except AlphabetException:
        req.write('<script type="text/javascript">document.getElementById("alpha").style.display = "block";</script>\n')
    except MultiFastaException:
        req.write('<script type="text/javascript">document.getElementById("multi").style.display = "block";</script>\n')
    except NoFastaException:
        req.write('<script type="text/javascript">document.getElementById("nofasta").style.display = "block";</script>\n')
    except LargeFastaException:
        req.write('<script type="text/javascript">document.getElementById("largefasta").style.display = "block";</script>\n')
    except Exception:
        req.write('<script type="text/javascript">document.getElementById("internal").style.display = "block";</script>\n')
        stream = StringIO()
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=stream)
        e = stream.getvalue()
        req.log_error("Traceback {trace} for uri {uri}\nunparsed_uri {unparsed_uri}\npath_info {path_info}\nargs {args}\ncontent_encoding={content_encoding}".format(trace=e, uri=str(req.uri), unparsed_uri=str(req.unparsed_uri), path_info=str(req.path_info), args=str(req.args), content_encoding=req.content_encoding), mod_python.apache.APLOG_ALERT)
    finally:
        req.write('<script type="text/javascript">document.getElementById("Begin").style.display = "none";</script>\n')
# def waithandle(req):
#     """
#     manage waiting for a job
#     """
#
#     # get the hash of the job from the request
# #    hash = req.args
#     form = mod_python.util.FieldStorage(req, keep_blank_values = 1)
#     hash = form.getfirst("hash")
#     # determine the jobs in the queue and in the workon list
#     found = ""
#
#     # check if
#     # - the job is in the queue (and where) or currently processed
#     #   -> write appropriate msg
#     # - finished -> redirect to result
#     # - not found -> write error
# #    f = open("%s/.lock" % (CONFIG.WRKPATH), "w")
# #    os.chmod("%s/.lock" % (CONFIG.WRKPATH), 0775)
# #    fcntl.flock(f.fileno(), fcntl.LOCK_EX)
#
#     write_reload = True
#     if hash == None:
#         found = "Ooops. Something went wrong. It seems that no jobID was set!<br>\n"
#         found += "Please contact us.<br>\n"
#         write_reload = False
#     elif exists(CONFIG.WRKPATH + "/" + hash + ".job"):
#         queued = glob.glob(CONFIG.WRKPATH + "/*.job")
#         queued.sort(key = lambda x: getmtime(x))
#
#         idx = queued.index(CONFIG.WRKPATH + hash + ".job")
#
#         found = "Your job is on position %d in the queue.<br>\n" % (idx + 1)
#         found += "<a href=\"modify.py?hash=%s\">Click here to DELETE your job!</a><br>\n" % (hash)
#         write_reload = True
#     elif exists(CONFIG.WRKPATH + "/" + hash + ".wrk"):
#         found = "Your sequence is currently being analyzed.<br>\n"
#         write_reload = True
#     elif os.path.exists(CONFIG.TOMCATPATH + hash + "/result"):
#         found = "Your job is complete. You will be forwarded to the results.<br>\n"
#         found += '<script type="text/javascript">window.setTimeout("location.replace(\\"./result.py?hash=%s\\")", 5000);</script>' % (hash)
#         write_reload = False
#     else:
#         found = "We can not find the specified ID!<br>\n"
#         found += "Please contact us if this is unexpected.<br>\n"
#         write_reload = False
#
# #    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
# #    f.close()
#     if write_reload:
#         f = open("%swait.txt" % (CONFIG.MITOSPATH))
#         found += f.read()
#         f.close()
#
#     req.write(webserver.makeMitos(found, 1, track = ""))
