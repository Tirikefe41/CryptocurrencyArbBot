
function sendReq(){
	cl = confirm("Do you wish to submit parameters!");
	if(cl){
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				data = this.responseText;
				
			}
		};
		
		xhttp.open("POST", "", true);
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhttp.send("apikey="+apikey.value+"&apisecret="+apisecret.value+"&buy_percentage="+buy_percentage.value+"&sell_percentage="+sell_percentage.value+"&percent_range="+percent_range.value+"&fixedbuy="+fixedbuy.value+"&max_daily_trades="+max_daily_trades.value);
	}
}

function clearLogs(){
	cl = confirm("Do you wish to clear logs!");
	if(cl){
		logs_list_info.innerHTML = "<p>Log is Empty!</p>";
		
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (this.readyState == 4 && this.status == 200) {
				lglist = this.responseText;
				LOGS = {};
				log_list.innerHTML = "";
			}
		};
		
		xhttp.open("GET", "clearlogs", true);
		xhttp.send();
	}
}

function toogleSettingsBtn(){
	if(settingsBtn.innerHTML == "Save"){
		settingsBtn.innerHTML = "Edit";
		apikey.setAttribute("disabled", "disabled");
		apisecret.setAttribute("disabled", "disabled");
		buy_percentage.setAttribute("disabled", "disabled");
		sell_percentage.setAttribute("disabled", "disabled");
		percent_range.setAttribute("disabled", "disabled");
		fixedbuy.setAttribute("disabled", "disabled");
		max_daily_trades.setAttribute("disabled", "disabled");

		validatePercentageInput();
		errmsg = error_msg.innerHTML;
		console.log(errmsg);
		if(errmsg != ""){
			errmsg = errmsg.replace("<br>", " and ");
			errmsg = errmsg.replace("<br>", "");
			alert(errmsg);

		}else{
			sendReq();
		}
		
	}else{
		settingsBtn.innerHTML = "Save";
		apikey.removeAttribute("disabled")
		apisecret.removeAttribute("disabled")
		buy_percentage.removeAttribute("disabled")
		sell_percentage.removeAttribute("disabled")
		percent_range.removeAttribute("disabled")
		fixedbuy.removeAttribute("disabled")
		max_daily_trades.removeAttribute("disabled")
	}
	
}

function validatePercentageInput(){
	spv = parseInt(sell_percentage.value);
	err = "";
	if(percentageChecker(spv) == false) err += "Invalid Percentage Increase Value!<br>";
	error_msg.innerHTML = err;
}

function percentageChecker(val){
	if(val < 0 || val > 100 || val.toString() == "NaN"){
		return false;

	}else{
		return true;
	}
}

