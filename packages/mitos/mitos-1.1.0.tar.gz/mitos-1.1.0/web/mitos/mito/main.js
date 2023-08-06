function validateEmail(email) {
	var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
	if( !emailReg.test( email ) ) {
		return false;
	} else {
		return true;
	}
}

function button01() {
	
	if(document.mtdb.email.value =="" || document.mtdb.email.value =="None" ) {
		document.mtdb.email.value = "None"
	}else if( ! validateEmail( document.mtdb.email.value ) ){
		alert("Invalid email adress");
		return;
	}


	if(document.mtdb.name.value =="") {
        	document.mtdb.name.value = "MITOS user"
	}
 	if(document.mtdb.myFile.value=="") {
 	   	alert("Empty file!")
 	   	return; 
 	}

	// check the values of the number input fields 
	// - get the value 
	// - check for unparseable input and range
	// - reassign parsed number (if e.g. '100xyz' input then 100 is parsed and reassigned)
	value = parseFloat(document.mtdb.evalue.value)
	if( isNaN( value ) || value < 1 ) {
		alert("The 'BLAST E-value Exponent' musst be a Number and at least 1")
		return;
	}
	document.mtdb.evalue.value = value

	value = parseFloat(document.mtdb.cutoff.value)
	if( isNaN(value) || value < 0 || value > 100 ) {
		alert("The 'Cutoff' musst be a Number between 0 and 100.")
		return;
	}
	document.mtdb.cutoff.value = value

	value = parseFloat(document.mtdb.maxovl.value)
	if( isNaN(value) || value < 0 || value > 100 ) {
		alert("The 'Maximum Overlap' musst be a Number between 0 and 100.")
		return;
	}
	document.mtdb.maxovl.value = value

	value = parseFloat(document.mtdb.fragovl.value)
	if( isNaN(value) || value < 0 || value > 100 ) {
		alert("The 'Fragment Overlap' musst be a Number between 0 and 100.")
		return;
	}
	document.mtdb.fragovl.value = value

	value = parseFloat(document.mtdb.clipfac.value)
	if( isNaN(value) || value < 1) {
		alert("The 'Clipping Factor' musst be a Number and at least 1")
		return;
	}
	document.mtdb.clipfac.value = value

	value = parseFloat(document.mtdb.fragfac.value)
	if(isNaN(value) || value < 1) {
		alert("The 'Fragment Quality Factor' musst be a Number and at least 1")
		return;
	}
	document.mtdb.fragfac.value = value

	value = parseFloat(document.mtdb.ststrange.value)
	if(isNaN(value) || value < 0){
		alert("The 'Start/Stop Range' musst be a Number and at least 0")
		return;
	}
	document.mtdb.ststrange.value = value

	value = parseFloat(document.mtdb.finovl.value)
	if(isNaN(value) || value < 0) {
		alert("The 'Final Maximum Overlap' musst be a Number and at least 0")
		return;
	}
	document.mtdb.finovl.value = value

	document.mtdb.submit()
}

var simple = 1

function showall() {
	if (simple == 1) {
		$(".hidein ").fadeIn(300)
		simple = 0
		$("#advance").toggleClass("simple advanced")
	}
	else {
		$(".hidein ").fadeOut(300)
		simple = 1
		$("#advance").toggleClass("simple advanced")
		$("input:checkbox").val(["on"])
		$("input[name=evalue]").val(2)
		$("input[name=cutoff]").val(50)
		$("input[name=maxovl]").val(20)
		$("input[name=clipfac]").val(10)
		$("input[name=fragovl]").val(20)
		$("input[name=fragfac]").val(10)
		$("input[name=ststrange]").val(6)
		$("input[name=finovl]").val(35)
		
		
	}
	
}

