/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

// colors from https://www.google.com/design/spec/style/color.html#color-color-palette
var colors = [
	'#F44336', //  0 red
	'#673AB7', //  1 deep purple
	'#03A9F4', //  2 light blue
	'#4CAF50', //  3 green
	'#FFEB3B', //  4 yellow
	'#FF5722', //  5 deep orange
	'#607D8B', //  6 blue grey
	'#E91E63', //  7 pink
	'#3F51B5', //  8 indigo
	'#00BCD4', //  9 cyan
	'#8BC34A', // 10 light green
	'#FFC107', // 11 amber
	'#795548', // 12 brown
	'#000000', // 13 black
	'#9C27B0', // 14 purple
	'#2196F3', // 15 blue
	'#009688', // 16 teal
	'#CDDC39', // 17 lime
	'#FF9800', // 18 orange
	'#9E9E9E'  // 19 grey
	];

function DiscussionBarometer(){
	'use strict';


	/**
	 * Displays the barometer
	 */
	this.showBarometer = function(){
		var uid = 0, uid_array = [],
			url = window.location.href.split('?')[0],
			splitted = url.split('/'),
			adress = 'position';

		// parse url
		if (url.indexOf('/attitude/') != -1){
			adress = 'attitude';
			uid = splitted[splitted.length-1];
			new DiscussionBarometer().ajaxRequest(uid, adress);
		} else if (url.indexOf('/justify/') != -1 || window.location.href.indexOf('/choose/') != -1) {
			adress = 'justify';
			$('#discussions-space-list li:not(:last-child) input').each(function(){
				uid_array.push($(this).attr('id').substr(5));
			});
			new DiscussionBarometer().ajaxRequest(uid_array, adress);
		} else if (url.indexOf('/reaction/') != -1){
			adress = 'argument';
			uid = splitted[splitted.length-3];
			new DiscussionBarometer().ajaxRequest(uid, adress);
		} else {
			adress = 'position';
			$('#discussions-space-list li:not(:last-child) label').each(function(){
				uid_array.push($(this).attr('id'));
			});
			new DiscussionBarometer().ajaxRequest(uid_array, adress);
		}
	};

	/**
	 * Requests JSON-Object
	 * @param uid: current id in url
	 * @param adress: keyword in url
	 */
	this.ajaxRequest = function(uid, adress){
		var dataString;
		switch(adress){
			case 'attitude':
				dataString = {is_argument: 'false', is_attitude: 'true', is_reaction: 'false', is_position: 'false', uids: uid};
				break;
			case 'justify':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'argument':
				dataString = {is_argument: 'true', is_attitude: 'false', is_reaction: 'true', is_position: 'false', uids: uid};
				break;
			case 'position':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'true', uids: JSON.stringify(uid)};
		}

		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			type: 'GET',
			dataType: 'json',
			data: dataString,
			async: true
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data, adress);
		}).fail(function () {
			new DiscussionBarometer().callbackIfFailForGetDictionary();
		});
	};

	/**
	 * Callback if the ajax request was successfull
	 * @param data: unparsed data of the request
	 * @param adress: step of the discussion
	 */
	this.callbackIfDoneForGetDictionary = function(data, adress){
		var obj, _db = new DiscussionBarometer();
        try{
	        obj = JSON.parse(data);
			console.log(obj);
        } catch(e) {
	        // TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
			alert('parsing-json: ' + e);
	        return;
        }
		$('#' + popupConfirmDialogId).modal('show');
		$('#' + popupConfirmDialogId + ' div.modal-body')
			.html('<canvas id="chartCanvas" width="400" height="400" style= "display: block; margin: 0 auto;"></canvas>');
		$('#' + popupConfirmDialogAcceptBtn).show().click( function () {
			$('#' + popupConfirmDialogId).modal('hide');
		}).removeClass('btn-success');
		$('#' + popupConfirmDialogRefuseBtn).hide();


		switch(adress){
			case 'attitude': _db.createAttitudeBarometer(obj); break;
			case 'position': _db.createStatementBarometer(obj); break;
			case 'justify':  _db.createStatementBarometer(obj); break;
			case 'argument': _db.createArgumentBarometer(obj); break;
		}
		$('#' + popupConfirmDialogId).find('.modal-title').text(obj.title);
	};

	/**
	 * Creates chart for attitude
	 * @param obj: parsed JSON-object
	 */
	this.createAttitudeBarometer = function(obj) {
		$('#' + popupConfirmDialogId + ' h4.modal-title').html(obj.text);
    	var ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d");

		var pieData = [
        {
			value: obj.agree_users.length,
        	color: colors[3],
			highlight: colors[10],
            label: 'agree'
        },
		{
			value: obj.disagree_users.length,
        	color: colors[0],
			highlight: colors[5],
			label: 'disagree'
		}
		];

		if (obj.agree_users.length + obj.disagree_users.length == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		} else {
			var chart = new Chart(ctx).Pie(pieData);
		}
	};

	/**
	 * Creates chart for statement
	 * @param obj: parsed JSON-object
	 */
	this.createStatementBarometer = function(obj) {
		var ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d"),
			chart = new Chart(ctx).Pie(),
			index = 0,
			users = 0;
		$.each(obj.opinions, function(key,value){
			if (value.text != null) {
				chart.addData({
					value: value.users.length,
					color: colors[index],
					label: value.text
				});
				users += value.users.length;
				index += 1;
			}
		});

		if (users == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		}
	};

	/**
	 * Creates chart for argument
	 * @param obj: parsed JSON-object
	 */
	this.createArgumentBarometer = function(obj) {
		var ctx = $('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").get(0).getContext("2d"),
			chart = new Chart(ctx).Pie(),
			index = 0,
			users = 0;
		$.each(obj.opinions, function(key, entry) {
			if(key != 'error') {
				chart.addData({
					value: entry.users.length,
					color: colors[index],
					label: entry.text
				});
				users += entry.users.length;
				index += 1;
			}
		});

		if (users == 0){
			this.setAlertIntoDialog();
			$('#' + popupConfirmDialogId + ' div.modal-body ' + "#chartCanvas").remove();
		}
	};

	this.setAlertIntoDialog = function(){
		var div, strong, span;
		div = $('<div>').attr('class', 'alert alert-dismissible alert-info');
		strong = $('<strong>').text('Ohh...! ');
		span = $('<span>').text(_t(noDecisionstaken));
		div.append(strong).append(span);
		$('#' + popupConfirmDialogId + ' div.modal-body').append(div);
		$('#' + popupConfirmDialogId).on('hidden.bs.modal', function (e) {
			div.remove();
		});
	};

	/**
	 * Callback if the ajax request failed
	 */
	this.callbackIfFailForGetDictionary = function(){
		alert('ajax-request: some error');
		// TODO: Um die Anzeige einer Fehlermeldung kümmern wir uns später.
	};
}
