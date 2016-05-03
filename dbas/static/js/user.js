/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(function () {
	'use strict';

	// send notification to users
	$('#send-notification').each(function () {
		$(this).click(function () {
			var _this = $(this);
			$('#popup-writing-notification-recipient').hide();
			$('#popup-writing-notification').modal('show');
			$('#popup-writing-notification-success').hide();
			$('#popup-writing-notification-failed').hide();
			$('#popup-writing-notification-send').click(function () {
				var url = window.location.href,
					splitted = url.split('/'),
					recipient;
				if (url.indexOf('/user/') != -1) {
					recipient = splitted[splitted.length - 1];
				} else {
					recipient = _this.prev().text();
				}
				sendNotification(recipient.trim()); // declared in notification.js
			});
		});
	});

	new User().getPublicUserData();
});

$(document).on({
	ajaxStart: function ajaxStartFct () { setTimeout("$('body').addClass('loading')", 0);},
	ajaxStop: function ajaxStopFct () { setTimeout("$('body').removeClass('loading')", 0);}

});
function User() {
	// https://www.google.com/design/spec/style/color.html#color-color-palette
	// 0 is Blue
	// 1 is Teal
	// 2 is Deep Orange
	// 3 is Brown
	var fillColorSet = ['rgba(187,222,251,0.4)', 'rgba(178,223,219,0.4)', 'rgba(255,204,188,0.4)', 'rgba(215,204,200,0.4']; //100
	var strokeColorSet = ['#2196F3', '#009688', '#FF5722', '#795548']; // 500
	var pointStrokeColorSet = ['#1565C0', '#00695C', '#D84315', '#4E342E']; // 800

	this.getPublicUserData = function () {
		$.ajax({
			url: 'ajax_get_public_user_data',
			method: 'GET',
			data:{'nickname': $('#public_nick').text()},
			dataType: 'json',
			async: true
		}).done(function getPublicUserDataDone(data) {
			new User().callbackDone(data);
		}).fail(function getPublicUserDataFail() {
			new User().callbackFail();
		});
	};

	this.callbackDone = function(jsonData){
		var parsedData = $.parseJSON(jsonData);
		this.createChart(parsedData, $('#user-activity-chart-space'), 'user-activity-canvas', 0);
		this.createChart(parsedData, $('#user-vote-chart-space'), 'user-vote-canvas', 1);
		this.createChart(parsedData, $('#user-statement-chart-space'), 'user-statement-canvas', 2);
		this.createChart(parsedData, $('#user-edit-chart-space'), 'user-edit-canvas', 3);
		this.setLegendCSS();
	};

	this.createChart = function(parsedData, space, id, count){
		var ctx, chart, data, div_legend;

		space.append('<canvas id="' + id + '" width="500" height="300" style= "display: block; margin: 0 auto;"></canvas>');
		ctx = document.getElementById(id).getContext('2d');
		data = {
			labels : parsedData['labels' + (count+1)],
			datasets : [{
				label: parsedData['label' + (count+1)],
				fillColor : fillColorSet[count],
				strokeColor : strokeColorSet[count],
				pointStrokeColor : pointStrokeColorSet[count],
				pointColor : "#fff",
				data : parsedData['data' + (count+1)],
				hover: {mode: 'single'}
			}]};
		chart = new Chart(ctx).Line(data);
		div_legend = $('<div>').addClass('chart-legend').append(chart.generateLegend());
		space.prepend(div_legend);
	};

	this.setLegendCSS = function() {
		var legend = $('.chart-legend');

		legend.find('ul').css({
			'list-style-type': 'none',
		});
		legend.find('li').css({
			'clear' : 'both',
			'padding': '2px'

		});
		legend.find('span').css({
			'border-radius': '4px',
			'padding': '0.2em',
			'color': 'white'
		}).addClass('lead');
	};

	this.getPublicUserDataFail = function(){
		alert('fail');
	};



}