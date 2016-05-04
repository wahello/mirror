/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AdminInterface(){

	/**
	 * Requests all attacks
	 */
	this.getArgumentOverview = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), _this = this;

		$.ajax({
			url: 'argument_overview',
			method: 'GET',
			dataType: 'json',
			data: { issue: new Helper().getCurrentIssueId() },
			async: true,
			headers: {'X-CSRF-Token': csrfToken}

		}).done(function getArgumentOverviewDone(data) { // display fetched data
			_this.setArgumentOverviewDataContent($.parseJSON(data));
			$('#' + listAllArgumentId).val(_t(hideAllArguments));
			$('#' + adminsSpaceForArgumentsId).fadeIn();
			new GuiHandler().hideErrorDescription();

		}).fail(function getArgumentOverviewFail() { // display error message
			var message = _t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 10). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.';
			new GuiHandler().showDiscussionError(message);
			$('#' + listAllArgumentId).val(_t(showAllArguments));
			$('#' + adminsSpaceForArgumentsId).fadeOut();
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setArgumentOverviewDataContent = function (jsonData) {
		var space = $('#' + adminsSpaceForArgumentsId),
			list = $('#dropdown-issue-list');

		space.empty();
		list.find('li:not(:first-child)').remove();
		$('#issue-switch-col').show();

		// add each issue table
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			list.append($('<li>').addClass('enabled').append($('<a>').text(key).attr('href', '#')));

			if (value.length == 0){
				var p = $('<p>').text(_t(noEntriesFor) + ': ' + key),
					div = $('<div>').attr('id', 'table_' + key.replace(/\ /g, '_'))
						.addClass('alert-warning')
						.addClass('alert')
						.attr('style', 'margin-left: 2em; margin-right: 2em; display: none');
				div.append(p);
				space.append(div);
				return;
			}

			var tableElement, i, img,
				tbody = $('<tbody>'),
				thead = $('<thead>'),
				trElement = $('<tr>'),
				tdElement = ['', '', '', '', '', ''],
				spanElement = ['', '', '', '', '', ''];

			// table element
			tableElement = $('<table>').attr('id', 'table_' + key.replace(/\ /g, '_'))
				.attr('class', 'table table-condensed tablesorter')
				.attr('border', '0')
				.attr('style', 'border-collapse: separate; border-spacing: 0px; display: none; margin-left: 1em; margin-right: 1em;');

			// header elements
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
				spanElement[i] = $('<spand>').attr('class', 'font-semi-bold');
			}

			// add header row
			spanElement[0].text('ID');
			spanElement[1].text(_t(text));
			spanElement[2].text('#Votes');
			spanElement[3].text('#Upvotes');
			spanElement[4].text('#Valid Upotes');
			spanElement[5].text('');

			// adding everyhting
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i].append(spanElement[i]);
				trElement.append(tdElement[i]);
				thead.append(trElement);
			}
			tableElement.append(thead);

			// add argument elements
			$.each(value, function setJsonArgumentDataToAdminContentEach(index, v_value) {
				trElement = $('<tr>');
				for (i = 0; i < tdElement.length; i += 1) {
					tdElement[i] = $('<td>');
				}

				img = $('<img>').addClass('glyphicon-local center info-glyphicon');
				img.attr('id', 'info_' + v_value.uid).attr('src', mainpage + "static/images/transparent.gif");
				img.click(function () {
					alert('todo infos about argument ' + v_value.uid);
				});

				tdElement[0].text(v_value.uid).attr('argument_' + v_value.uid);
				tdElement[1].text(v_value.text);
				tdElement[2].text(v_value.votes);
				tdElement[3].text(v_value.valid_votes);
				tdElement[4].text(v_value.valid_upvotes);
				tdElement[5].append(img);

				for (i = 0; i < tdElement.length; i += 1)
					trElement.append(tdElement[i]);

				trElement.hover(function () {
					$(this).toggleClass('text-hover');
				});

				tbody.append(trElement);
			});
			tableElement.append(tbody);
			space.append(tableElement);
		});

		// some magic and gui fixes for the issue dropdown
		space.children().eq(0).show();
		list.find('li:nth-child(1)').removeClass('enabled').addClass('disabled');
		list.find('li').each(function(){
			$(this).click(function(){
				var current = $('#dropdown-issue-list').find('li.disabled'),
					currentIssue = current.find('a').text();
				current.addClass('enabled').removeClass('disabled');
				$(this).removeClass('enabled').addClass('disabled');
				$('#table_' + currentIssue.replace(/\ /g, '_')).hide();
				$('#table_' + $(this).find('a').text().replace(/\ /g, '_')).show();
				alert('#table_' + currentIssue.replace(/\ /g, '_') + "\n" + '#table_' + $(this).find('a').text().replace(/\ /g, '_'))
			})
		});
	};
}

/**
 * Class for the click events in the navigation bar on the left side
 * @constructor
 */
function NavBarInterface(){
	var _this = this;
	this.setUpLinks = function(){
		$('#admin-dashboards').click(function(){	_this.showDashboard();	});
		$('#admin-users').click(function(){			_this.showUsers();		});
		$('#admin-arguments').click(function(){		_this.showArguments()	});
		$('#dashboard-user-count-detail').click(function(){			_this.showUsers();		});
		$('#dashboard-vote-count-detail').click(function(){			_this.showVotes();		});
		$('#dashboard-argument-count-detail').click(function(){		_this.showArguments();	});
		$('#dashboard-statement-count-detail').click(function(){	_this.showStatements();	});
	};

	/**
	 * Set everything to the default view
	 */
	this.hideEverything = function(){
		$('#navbar-wrapper').find('.active').removeClass('active');
		$('#content-wrapper').find('>div').each(function(){
			$(this).hide();
		});
	};

	/**
	 * Shows the dashboard alias overview
	 */
	this.showDashboard = function(){
		this.hideEverything();
		$('#admin-dashboards').parent().addClass('active');
		$('#admins-space-dashboard').show();
	};

	/**
	 * Shows the user space
	 */
	this.showUsers = function(){
		this.hideEverything();
		$('#admin-users').parent().addClass('active');
		$('#admins-space-users').show().prev();
	};

	/**
	 * Shows the voting space
	 */
	this.showVotes = function(){
		this.hideEverything();
		// TODO
	};

	/**
	 * Shows the argument space
	 */
	this.showArguments = function(){
		this.hideEverything();
		$('#admin-arguments').parent().addClass('active');
		$('#admins-space-argument').prev().show();
	};

	/**
	 *
	 */
	this.showStatements = function(){
		this.hideEverything();
		// TODO
	};
}

// main function
$(function () {
	var ai = new AdminInterface(), nbi = new NavBarInterface();

	// hide or show all users
	$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
		if ($(this).val() === _t(showAllUsers)) {
			$('#admins-space-users').fadeIn();
			$(this).val(_t(hideAllUsers));
		} else {
			$('#admins-space-users').fadeOut();
			$(this).val(_t(showAllUsers));
		}
	});

	// hide or show all arguments
	$('#' + listAllArgumentId).click(function listAllUsersAttacksId() {
		if ($(this).val() === _t(showAllArguments)) {
			// getting arguments via ajax, if we do not fetched them already
			if ($('#' + adminsSpaceForArgumentsId).find('table').length == 0) {
				ai.getArgumentOverview();
			} else {
				$('#' + listAllArgumentId).val(_t(hideAllArguments));
				$('#' + adminsSpaceForArgumentsId).fadeIn();
			}
		} else {
			$('#' + adminsSpaceForArgumentsId).fadeOut();
			$('#' + listAllArgumentId).val(_t(showAllArguments));
		}
	});

	nbi.setUpLinks();
});
