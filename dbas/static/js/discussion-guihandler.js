/*global $, jQuery, discussionsDescriptionId, discussionContainerId, discussionSpaceId, discussionAvoidanceSpaceId, _t */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function GuiHandler() {
	'use strict';
	var interactionHandler;

	this.setHandler = function (externInteractionHandler) {
		interactionHandler = externInteractionHandler;
	};

	/**
	 * Setting a description in some p-tag without mouse over
	 * @param text to set
	 */
	this.setDiscussionsDescription = function (text) {
		$('#' + discussionsDescriptionId).html(text).attr('title', text);
	};

	/**
	 * Setting a description in some p-tag with mouse over
	 * @param text to set
	 * @param mouseover hover-text
	 * @param additionalAttributesAsDict additional attribute
	 */
	this.setDiscussionsDescription = function (text, mouseover, additionalAttributesAsDict) {
		$('#' + discussionsDescriptionId).html(text).attr('title', mouseover);
		if (additionalAttributesAsDict !== null)
			$.each(additionalAttributesAsDict, function setDiscussionsDescriptionEach(key, val) {
				$('#' + discussionsDescriptionId).attr(key, val);
			});
	};

	/**
	 * Setting a description in some p-tag
	 * @param text to set
	 */
	this.setDiscussionAttackDescription = function (text) {
		$('#' + discussionAttackDescriptionId).html(text);
	};

	/**
	 * Setting an error description in some p-tag
	 * @param text to set
	 */
	this.setErrorDescription = function (text) {
		$('#' + discussionErrorDescriptionId).html(text);
	};

	/**
	 * Setting a success description in some p-tag
	 * @param text to set
	 */
	this.setSuccessDescription = function (text) {
		$('#' + discussionSuccessDescriptionId).text(text);
	};

	/**
	 * Sets the visibility of the island view conainter
	 * @param shouldBeVisibile true, when it should be visible
	 * @param currentStatementText current user statement
	 */
	this.setVisibilityOfDisplayStyleContainer = function (shouldBeVisibile, currentStatementText) {
		if (shouldBeVisibile) {
			$('#' + displayControlContainerId).fadeIn('slow');
			$('#' + islandViewContainerH4Id).html(_t(islandViewHeaderText) + ' <b>' + currentStatementText + '</b>');
		} else {
			$('#' + displayControlContainerId).hide();
		}
	};

	/**
	 * Sets an "add statement" button as content
	 * @param val will be used as value
	 * @param isArgument if true, argumentButtonWasClicked is used, otherwise
	 */
	this.setNewArgumentButtonOnly = function (val, isArgument) {
		var listitem = [];
		listitem.push(new Helper().getKeyValAsInputInLiWithType(addReasonButtonId, val, isArgument, false, false, ''));
		new GuiHandler().addListItemsToDiscussionsSpace(listitem);
	};

	/**
	 * Displays given data in the island view
	 * @param jsonData json encoded dictionary
	 */
	this.displayDataInIslandView = function (jsonData) {
		var liElement, ulProElement, ulConElement;
		ulProElement = $('<ul>');
		ulConElement = $('<ul>');

		// get all values as text in list
		$.each(jsonData, function displayDataInIslandViewEach(key, val) {
			// is there a con or pro element?
			if (key.indexOf('pro') == 0) {
				liElement = $('<li>');
				liElement.text(val.text);
				ulProElement.append(liElement);
			} else if (key.indexOf('con') == 0) {
				liElement = $('<li>');
				liElement.text(val.text);
				ulConElement.append(liElement);
			}
		});

		// append in divs
		$('#' + proIslandId).empty().append(ulProElement);
		$('#' + conIslandId).empty().append(ulConElement);

	};

	/**
	 * Appends all items in an ul list and this will be appended in the 'discussionsSpace'
	 * @param items list with al items
	 */
	this.addListItemsToDiscussionsSpace = function (items) {
		var ulElement;

		// wrap all elements into a list
		ulElement = $('<ul>');
		ulElement.append(items);

		// append them to the space
		$('#' + discussionSpaceId).append(ulElement);

		// hover style element for the list elements
		ulElement.children().hover(function () {
			$(this).toggleClass('table-hover');
		});
	};

	/**
	 * Adds a textarea with a little close button (both in a div tag) to a parend tag
	 * @param parentid id-tag of the parent element, where a textare should be added
	 * @param identifier additional id
	 * @param is_statement
	 */
	this.addTextareaAsChildInParent = function (parentid, identifier, is_statement) {
		/**
		 * The structure is like:
		 * <div><textarea .../><button...></button></div>
		 */
		var area, parent, div, div_content, button, span, childCount, div_dropdown;
		parent = $('#' + parentid);
		childCount = parent.children().length;

		div = $('<div>');
		div.attr({
			class: 'row',
			id: 'div' + childCount.toString()
		});

		div_content = $('<div>');
		div_content.attr({
			id: 'div-content-' + childCount.toString()
		});

		button = $('<button>');
		button.attr({
			type: 'button',
			class: 'close',
			id: 'button_' + identifier + childCount.toString()
		});

		span = $('<span>');
		span.html('&times;');

		area = $('<textarea>');
		area.attr({
			type: 'text',
			class: '',
			name: '',
			autocomplete: 'off',
			value: '',
			id: 'textarea_' + identifier + childCount.toString()
		});

		button.append(span);
		div_dropdown = this.getDropdownWithSentencesOpeners(identifier, childCount.toString());
		div_content.append(area);
		div_content.append(button);

		// remove everything on click
		button.attr({
			onclick: 'this.parentNode.parentNode.removeChild(parentNode);'
		});

		// add everything
		// TODO insert dropdown menu
		// div_dropdown.attr('class', 'col-md-3');
		// div_content.attr('class', 'col-md-9');
		div_content.attr('title', _t(textAreaReasonHintText));
		div.append(div_dropdown);
		div.append(div_content);
		parent.append(div);

		if (is_statement) {
			div_dropdown.show();
		} else {
			div_dropdown.hide();
		}

		this.setDropdownClickListener(identifier, childCount.toString());
	};

	/**
	 * Creates dropdown button
	 * @param identifier
	 * @param number
	 * @returns {jQuery|HTMLElement|*}
	 */
	this.getDropdownWithSentencesOpeners = function (identifier, number) {
		var dropdown, button, span, ul, li_content, li_header, i, a, btn_id, a_id, h = new Helper(),
			sentencesOpeners;
		sentencesOpeners = identifier == id_pro ? _t(sentencesOpenersArguingWithAgreeing) : _t(sentencesOpenersArguingWithDisagreeing);

		// div tag for the dropdown
		dropdown = $('<div>');
		dropdown.attr('id', 'div-' + identifier + '-dropdown-' + number);
		dropdown.attr('class', 'dropdown');

		// button with span element
		span = $('<span>');
		span.attr('class', 'caret');
		button = $('<button>');
		button.attr('class', 'btn btn-default dropdown-toggle ' + (identifier.toLowerCase() == 'left' ? 'btn-success' : 'btn-danger'));
		button.attr('type', 'button');
		btn_id = identifier + '-dropdown-sentences-openers-' + number;
		button.attr('id', btn_id);
		button.attr('data-toggle', 'dropdown');
		button.text(identifier.toLowerCase() == 'left' ? _t(agreeBecause) : _t(disagreeBecause));
		button.append(span);
		dropdown.append(button);

		ul = $('<ul>');
		ul.attr('class', 'dropdown-menu');
		ul.attr('role', 'menu');

		// first categorie
		li_header = $('<li>');
		li_header.attr('class', 'dropdown-header');
		li_header.text('Argue');
		ul.append(li_header);
		for (i = 0; i < sentencesOpeners.length; i++) {
			li_content = $('<li>');
			a_id = identifier + '-sentence-opener-' + i;
			a = h.getATagForDropDown(a_id, _t(clickToChoose) + ': ' + _t(sentencesOpeners[i]), _t(sentencesOpeners[i]));
			li_content.append(a);
			ul.append(li_content);
		}

		// second categorie
		li_header = $('<li>');
		li_header.attr('class', 'dropdown-header');
		li_header.text('Inform');
		ul.append(li_header);
		for (i = 0; i < sentencesOpenersInforming.length; i++) {
			li_content = $('<li>');
			a_id = identifier + '-sentence-opener-' + (sentencesOpeners.length + i);
			a = h.getATagForDropDown(a_id, _t(clickToChoose) + ': ' + _t(sentencesOpenersInforming[i]), _t(sentencesOpenersInforming[i]));
			li_content.append(a);
			ul.append(li_content);
		}

		// append everything
		dropdown.append(ul);

		return dropdown;
	};

	/**
	 *
	 * @param identifier
	 * @param number
	 */
	this.setDropdownClickListener = function (identifier, number) {
		var a_id, i, sentencesOpeners;
		sentencesOpeners = identifier == id_pro ? _t(sentencesOpenersArguingWithAgreeing) : _t(sentencesOpenersArguingWithDisagreeing);

		// add clicks
		for (i = 0; i < sentencesOpenersInforming.length + sentencesOpeners.length; i++) {
			a_id = identifier + '-sentence-opener-' + i;
			$('#' + a_id).click(function () {
				$('#' + identifier + '-dropdown-sentences-openers-' + number).html($(this).text() + '<span class="caret"></span>');
			});
		}
	};

	/**
	 * Sets the new position as list child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setNewStatementAsLastChild = function (jsonData) {
		if (jsonData.result === 'failed') {
			if (jsonData.reason === 'empty text') {
				this.setErrorDescription(_t(notInsertedErrorBecauseEmpty));
			} else if (jsonData.reason === 'duplicate') {
				this.setErrorDescription(_t(notInsertedErrorBecauseDuplicate));
			} else {
				this.setErrorDescription(_t(notInsertedErrorBecauseUnknown));
			}
		} else {
			var newElement = new Helper().getKeyValAsInputInLiWithType(jsonData.statement.uid, jsonData.statement.text, true, false, false, '');
			newElement.children().hover(function () {
				$(this).toggleClass('table-hover');
			});
			$('#li_' + addReasonButtonId).before(newElement); // TODO.slideDown('slow').attr('checked', false);
			new GuiHandler().setSuccessDescription(_t(addedEverything));

		}
	};

	/**
	 * Sets the new premisses as list child in discussion space or displays an error
	 * @param jsonData returned data
	 */
	this.setPremissesAsLastChild = function (jsonData) {
		var newElement = '', helper = new Helper(), text, tmp='', l, keyword, attack, same_group, premissegroup_uid = '0';

		// premisse group?
		same_group = jsonData.same_group == '1';
		// are we positive or negative?
		attack = $('#' + discussionsDescriptionId).attr('attack');
		if (typeof attack !== typeof undefined && attack !== false){
			keyword = attack.indexOf(attr_undermine) != -1 || attack.indexOf(attr_undercut) != -1 ? 'con' : 'pro';
		} else {
			keyword = 'pro';
		}

		$.each(jsonData, function setPremissesAsLastChildEach(key, val) {
			if (key.substr(0, 3) == keyword) {
				if (!same_group) {
					text = _t(because) + ' ' + val.text;
					l = text.length - 1;
					if (text.substr(l) != '.' && text.substr(l) != '?' && text.substr(l) != '!') {
						text += '.';
					}

					newElement = helper.getKeyValAsInputInLiWithType(val.premissegroup_uid, text, false, true, false, val.text);
					newElement.children().hover(function () {
						$(this).toggleClass('table-hover');
					});
					$('#li_' + addReasonButtonId).before(newElement);
				} else {
					alert("How to handle pgroups? Look at 'changelog and edit'");
					// TODO how to handle inserting pgroups? Look at 'changelog and edit'
					text = val.text;
					l = text.length - 1;
					if (text.substr(l) == '.' || text.substr(l) == '?' || text.substr(l) == '!') {
						text = text.substr(0,l);
					}

					if (tmp == ''){
						tmp = _t(because) + ' ' + text;
						premissegroup_uid = val.premissegroup_uid;
					} else {
						tmp += ' ' + _t(and) + ' ' + text
					}
				}
			} else if (key.substr(0, 3) == 'con') {
				// todo setPremissesAsLastChild contra premisses
			}
		});
		// add the group element, because we have not done this
		if (same_group){
			tmp += '.';
			newElement = helper.getKeyValAsInputInLiWithType(premissegroup_uid, tmp, false, true, false, tmp);
			newElement.children().hover(function () {
				$(this).toggleClass('table-hover');
			});
			$('#li_' + addReasonButtonId).before(newElement);
		}

		this.setDisplayStylesOfAddStatementContainer(false, false, false, false, false);
		$('#' + addReasonButtonId).attr('checked', false);

	};

	/**
	 * Set some style attributes,
	 * @param isVisible true, if the container should be displayed
	 * @param isStatement true, if we have an argument
	 * @param isStart
	 * @param isPremisse
	 * @param isArgument
	 */
	this.setDisplayStylesOfAddStatementContainer = function (isVisible, isStart, isPremisse, isStatement, isArgument) {
		var statement, attack, header,
			discussionsDescription = $('#' + discussionsDescriptionId),
			addStatementContainer = $('#' + addStatementContainerId),
			addReasonButton = $('#' + addReasonButtonId),
			addStatementContainerMainInputIntro = $('#' + addStatementContainerMainInputIntroId),
			relation = discussionsDescription.attr('attack'),
			guihandler = new GuiHandler(),
			ajaxhandler = new AjaxSiteHandler(),
			interactionhandler = new InteractionHandler();
		if (!isVisible) {
			addStatementContainer.fadeOut('slow');
			$('#' + addStatementContainerMainInputId).val('');
			addReasonButton.disable = false;
			return;
		}

		// isVisible == true:
		$('#' + proPositionTextareaId).empty();
		$('#' + conPositionTextareaId).empty();
		addStatementContainerMainInputIntro.text('');
		addStatementContainer.fadeIn('slow');
		$('#' + addStatementErrorContainer).hide();
		addReasonButton.disable = true;

		if (isStatement || typeof relation == 'undefined') {
			// some pretty print options
			if (isStart) {
				$('#' + addStatementContainerH4Id).text(_t(argumentContainerH4TextIfConclusion));
			} else {
				if (discussionsDescription.html().indexOf(_t(firstPremisseText1)) != -1){
					$('#' + addStatementContainerH4Id).html(_t(whyDoYouThinkThat) + ' <b>' + discussionsDescription.attr('text') + '<b>');
				} else if (discussionsDescription.html().indexOf(_t(otherParticipantsDontHave)) != -1) {
					var index1 = discussionsDescription.html().indexOf('<b>');
					var index2 = discussionsDescription.html().indexOf('</b>');
					header = discussionsDescription.html().substr(index1, index2-index1+5);
					$('#' + addStatementContainerH4Id).html(_t(whyDoYouThinkThat) + ' <b>' + header + '</b>');
				} else {
					$('#' + addStatementContainerH4Id).html(_t(argumentContainerH4TextIfPremisse) + '<br><br>' + discussionsDescription.html());
				}
				addStatementContainerMainInputIntro.text(_t(because) + '...');
			}

			// gui modifications
			$('#' + addStatementContainerMainInputId).show();
			$('#' + proPositionColumnId).hide();
			$('#' + conPositionColumnId).hide();
			// at the beginning we differentiate between statement and statements
			$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenStatement() {
				if (isStart) {
					ajaxhandler.sendNewStartStatement($('#' + addStatementContainerMainInputId).val());
				} else {
					ajaxhandler.sendNewStartPremisse($('#' + addStatementContainerMainInputId).val(), discussionsDescription.attr('conclusion_id'));
				}
				guihandler.setErrorDescription('');
				guihandler.setSuccessDescription('');
			});

		} else if (isPremisse || isArgument) {
			statement = discussionsDescription.attr('text');
			// $('#' + addStatementContainerH4Id).text(isPremisse ? _t(argumentContainerH4TextIfPremisse) :
			// _t(argumentContainerH4TextIfArgument));
			$('#' + addStatementContainerH4Id).text(_t(argumentContainerH4TextIfPremisse));
			$('#' + addStatementContainerMainInputId).hide().focus();

			// take a look, if we agree or disagree, and where we are
			if (relation.indexOf(attr_undermine) != -1) {this.showAddStatementsTextareasWithTitle(false, true, false, statement);
			} else if (relation.indexOf(attr_support) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, false, statement);
			} else if (relation.indexOf(attr_undercut) != -1) {	this.showAddStatementsTextareasWithTitle(false, true, true, statement);
			} else if (relation.indexOf(attr_overbid) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, true, statement);
			} else if (relation.indexOf(attr_rebut) != -1) {	this.showAddStatementsTextareasWithTitle(true, false, false, statement);
			} else {
				alert("Something went wrong in 'setDisplayStylesOfAddStatementContainer'");
			}

			// does other users have an opinion?
			if (isArgument) {
				if (discussionsDescription.text().indexOf(_t(otherParticipantsDontHave)) != -1) {
					// other users have no opinion, so the participant can give pro and con
					this.showAddStatementsTextareasWithTitle(true, true, false, statement);
				} else {
					// alert('Todo: How to insert something at this place?');
				}
			}

			$('#' + sendNewStatementId).off('click').click(function setDisplayStylesOfAddStatementContainerWhenArgument() {
				interactionhandler.getPremissesAndSendThem(false);
				guihandler.setErrorDescription('');
				guihandler.setSuccessDescription('');
				$('#' + addStatementErrorContainer).hide();
				$('#' + addStatementErrorMsg).text('');
			});
		} else {
			alert('What now (II)? GuiHandler: setDisplayStylesOfAddStatementContainer');
		}

		guihandler.addTextareaAsChildInParent(proPositionTextareaId, id_pro, isStatement);
		guihandler.addTextareaAsChildInParent(conPositionTextareaId, id_con, isStatement);
	};

	/**
	 *
	 * @param isAgreeing
	 * @param isDisagreeing
	 * @param isAttackingRelation
	 * @param title
	 */
	this.showAddStatementsTextareasWithTitle = function (isAgreeing, isDisagreeing, isAttackingRelation, title) {
		var extra = isAttackingRelation ? (' ' + _t(theCounterArgument)) : '';
		if (isAgreeing) {	 $('#' + proPositionColumnId).show(); } else { $('#' + proPositionColumnId).hide(); }
		if (isDisagreeing) { $('#' + conPositionColumnId).show(); } else { $('#' + conPositionColumnId).hide(); }

		// given colors are the HHU colors. we could use bootstrap (text-success, text-danger) instead, but they are too dark
		$('#' + headingProPositionTextId).html(isAgreeing ? ' I <span class=\'green-bg\'>agree</span> with' + extra +
			': <b>' + title + '</b>, because...' : '');
		$('#' + headingConPositionTextId).html(isDisagreeing ? ' I <span class=\'red-bg\'>disagree</span> with' + extra +
			': <b>' + title + '</b>, because...' : '');
	};

	/**
	 *
	 * @param parsedData
	 * @param callbackid
	 */
	this.setStatementsAsProposal = function (parsedData, callbackid){
		var callback = $('#' + callbackid), uneditted_value;
		// is there any value ?
		if (Object.keys(parsedData).length == 0){
			callback.next().empty();
			return;
		}

		var params, token, button, span_dist, span_text, statementListGroup, distance, index;
		callback.focus();
		statementListGroup = callback.next();
		statementListGroup.empty(); // list with elements should be after the callbacker
		// $('#' + statementListGroupId).empty();

		$.each(parsedData, function (key, val) {
			params = key.split('_');
			distance = parseInt(params[0]);
			index = params[1];

			token = callback.val();
			var pos = val.toLocaleLowerCase().indexOf(token.toLocaleLowerCase()), newpos = 0;
			var start = 0;

			// make all tokens bold
			uneditted_value = val;
			while (token.length>0 && newpos != -1){//val.length) {
				val = val.substr(0, pos) + '<b>' + val.substr(pos, token.length) + '</b>' + val.substr(pos + token.length);
				start = pos + token.length + 7;
				newpos = val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase());
				pos = start + (newpos > -1 ? val.toLocaleLowerCase().substr(start).indexOf(token.toLocaleLowerCase()) : 0);

				// val = val.replace(token, '<b>' + token + '</b>');
			}

			button = $('<button>').attr({type : 'button',
				class : 'list-group-item',
				id : 'proposal_' + index});
   			button.hover(function(){ $(this).addClass('active');
   			    	  }, function(){ $(this).removeClass('active');
   			});
			span_dist = $('<span>').attr({class : 'badge'}).text(_t(levenshteinDistance) + ' ' + distance);
			span_text = $('<span>').attr({id : 'proposal_' + index + '_text'}).html(val);
			button.append(span_dist).append(span_text).click(function(){
				callback.val(uneditted_value);
				statementListGroup.empty(); // list with elements should be after the callbacker
			});
			statementListGroup.append(button);
		});
		 // list with elements should be after the callbacker
		statementListGroup.prepend('<h4>' + _t(didYouMean) + '</h4>');
		//$('#' + statementListGroupId).prepend('<h4>' + didYouMean + '</h4>');
	};

	/**
	 * Restets the values of the add statement container to default.
	 */
	this.resetAddStatementContainer = function () {
		$('#' + proPositionTextareaId).empty();
		$('#' + conPositionTextareaId).empty();
	};

	/**
	 * Shows an error on discussion space as well as a retry button
	 * @param error_msg message of the error
	 */
	this.showDiscussionError = function (error_msg) {
		$('#' + discussionFailureRowId).fadeIn('slow');
		$('#' + discussionFailureMsgId).html(error_msg);
	};

	/**
	 * Check whether the edit button should be visible or not
	 */
	this.resetEditButton = function () {
		var is_editable = false, statement, uid, is_premisse, is_start;
		$('#' + discussionSpaceId + ' ul > li').children().each(function () {
			statement = $(this).val();
			uid = $(this).attr('id');
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');
			// do we have a child with input or just the label?
			if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {
				is_editable = true;
				return false; // break
			}
		});

		// do we have an statement there?
		if (is_editable) {
			$('#' + editStatementButtonId).fadeIn('slow');
		} else {
			$('#' + editStatementButtonId).fadeOut('slow');
		}
	};

	/**
	 * Opens the edit statements popup
	 */
	this.showEditStatementsPopup = function () {
		var table, tr, td_text, td_buttons, statement, uid, type, is_start, is_premisse, tmp, text_count, statement_id, text, i,
			helper = new Helper(), is_final, popupEditStatementSubmitButton = $('#' + popupEditStatementSubmitButtonId);
		$('#' + popupEditStatementId).modal('show');
		popupEditStatementSubmitButton.hide();
		$('#' + popupEditStatementWarning).hide();

		// each statement will be in a table with row: index, text, button for editing
		// more action will happen, if the button is pressed

		// top row
		table = $('<table>');
		table.attr({
			id: 'edit_statement_table',
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 5px 5px;'
		});
		tr = $('<tr>');
		td_text = $('<td>');
		td_buttons = $('<td>');
		td_text.html('<b>Text</b>').css('text-align', 'center');
		td_buttons.html('<b>Options</b>').css('text-align', 'center');
		tr.append(td_text);
		tr.append(td_buttons);
		table.append(tr);

		uid = 0;
		// append a row for each statement
		$('#' + discussionSpaceId + ' ul > li').children().each(function () {
			statement = $(this).val();
			if (statement.toLocaleLowerCase().indexOf(_t(because)) == 0){
				statement = new Helper().startWithUpperCase(statement.substring(8));
			}
			uid = $(this).attr('id');
			type = $(this).attr('class');
			is_premisse = $(this).hasClass('premisse');
			is_start = $(this).hasClass('start');

			// TODO edit premisse groups
			if (typeof uid != 'undefined' && uid.indexOf('_') != -1){
				tmp = uid.split('_');
				uid = tmp[tmp.length -1];
			}

			// do we have a child with input or just the label?
			if ($(this).prop('tagName').toLowerCase().indexOf('input') > -1 && statement.length > 0 && $.isNumeric(uid) || is_premisse || is_start) {

				// is this a premisse group with more than one text?
				if (typeof $(this).attr('text_count') !== typeof undefined && $(this).attr('text_count') !== false){
					text_count = $(this).attr('text_count');
					type = 'premissesgroup';

					for (i=1; i<=parseInt(text_count); i++) {
						statement_id = $(this).attr('text_' + i + '_statement_id');
						text = $(this).attr('text_' + i);
						tr = helper.createRowInEditDialog(statement_id, text, type);
						table.append(tr);
					}
				} else {
					tr = helper.createRowInEditDialog(uid, statement, type);
					table.append(tr);
				}
			}
		});

		$('#' + popupEditStatementContentId).empty().append(table);
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
		popupEditStatementSubmitButton.hide().click(function edit_statement_click() {
			statement = $('#' + popupEditStatementTextareaId).val();
			is_final = $('#' + popupEditStatementWarning).is(':visible');
			//$('#edit_statement_td_text_' + $(this).attr('statement_id')).text(statement);
			new AjaxSiteHandler().sendCorrectureOfStatement($(this).attr('statement_id'), $(this).attr('callback_td'), statement, is_final);
		});

		// on click: do ajax
		// ajax done: refresh current statement with new text
	};

	/**
	 * Display url sharing popup
	 */
	this.showUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('show');
		new AjaxSiteHandler().getShortenUrl(window.location);
		//$('#' + popupUrlSharingInputId).val(window.location);
	};

	/**
	 * Display url sharing popup
	 */
	this.showGeneratePasswordPopup = function () {
		$('#' + popupGeneratePasswordId).modal('show');
		$('#' + popupGeneratePasswordCloseButtonId).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
		$('#' + popupLoginCloseButton).click(function(){
			$('#' + popupGeneratePasswordId).modal('hide');
		});
	};

	/**
	 * Displays the edit text field
	 */
	this.showEditFieldsInEditPopup = function () {
		$('#' + popupEditStatementSubmitButtonId).fadeIn('slow');
		$('#' + popupEditStatementTextareaId).fadeIn('slow');
		$('#' + popupEditStatementDescriptionId).fadeIn('slow');
	};

	/**
	 * Hides the url sharing text field
	 */
	this.hideEditFieldsInEditPopup = function () {
		$('#' + popupEditStatementSubmitButtonId).hide();
		$('#' + popupEditStatementTextareaId).hide();
		$('#' + popupEditStatementDescriptionId).hide();
	};

	/**
	 * Hides the logfiles
	 */
	this.hideLogfileInEditPopup = function () {
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + popupEditStatementLogfileHeaderId).html('');
	};

	/**
	 * Closes the popup and deletes all of its content
	 */
	this.hideEditStatementsPopup = function () {
		$('#' + popupEditStatementId).modal('hide');
		$('#' + popupEditStatementContentId).empty();
		$('#' + popupEditStatementLogfileSpaceId).text('');
		$('#' + popupEditStatementLogfileHeaderId).text('');
		$('#' + popupEditStatementTextareaId).text('');
		$('#' + popupEditStatementErrorDescriptionId).text('');
		$('#' + popupEditStatementSuccessDescriptionId).text('');
	};

	/**
	 * Closes the popup and deletes all of its content
	 */
	this.hideUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('hide');
		$('#' + popupUrlSharingInputId).val('');
	};

	/**
	 * Displays all corrections in the popup
	 * @param jsonData json encoded return data
	 */
	this.displayStatementCorrectionsInPopup = function (jsonData) {
		var table, tr, td_text, td_date, td_author;

		// top row
		table = $('<table>');
		table.attr({
			id: 'edit_statement_table',
			class: 'table table-condensed',
			border: '0',
			style: 'border-collapse: separate; border-spacing: 5px 5px;'
		});
		tr = $('<tr>');
		td_date = $('<td>');
		td_text = $('<td>');
		td_author = $('<td>');
		td_date.html('<b>Date</b>').css('text-align', 'center');
		td_text.html('<b>Text</b>').css('text-align', 'center');
		td_author.html('<b>Author</b>').css('text-align', 'center');
		tr.append(td_date);
		tr.append(td_text);
		tr.append(td_author);
		table.append(tr);

		$.each(jsonData, function displayStatementCorrectionsInPopupEach(key, val) {
			tr = $('<tr>');
			td_date = $('<td>');
			td_text = $('<td>');
			td_author = $('<td>');

			td_date.text(val.date);
			td_text.text(val.text);
			td_author.text(val.author);

			// append everything
			tr.append(td_date);
			tr.append(td_text);
			tr.append(td_author);
			table.append(tr);
		});

		$('#' + popupEditStatementLogfileSpaceId).empty().append(table);
	};

	/**
	 * Dispalys the 'how to write text '-popup, when the setting is not in the cookies
	 */
	this.displayHowToWriteTextPopup = function(){
		var cookie_name = 'HOW_TO_WRITE_TEXT',
			// show popup, when the user does not accepted the cookie already
			userAcceptedCookies = new Helper().isCookieSet(cookie_name);

		if (!userAcceptedCookies) {
			$('#' + popupHowToWriteText).modal('show');
		}

		// accept cookie
		$('#' + popupHowToWriteTextOkayButton).click(function(){
			$('#' + popupHowToWriteText).modal('hide');
			new Helper().setCookie(cookie_name);
		});
	};

	/**
	 * Dispalys the 'how to write text '-popup, when the setting is not in the cookies
	 */
	this.displayPremisseGroupPopup = function(){
		var cookie_name = 'HOW_TO_SET_PREMISSEGROUPS',
			// show popup, when the user does not accepted the cookie already
			userAcceptedCookies = new Helper().isCookieSet(cookie_name);

		if (!userAcceptedCookies) {
			$('#' + popupHowToSetPremisseGroups).modal('show');
		}

		$('#' + popupHowToSetPremisseGroupsCloseButton).click(function(){
			$('#' + proTextareaPremissegroupCheckboxId).attr('checked', false);
			$('#' + conTextareaPremissegroupCheckboxId).attr('checked', false);
		});

		$('#' + popupHowToSetPremisseGroupsClose).click(function(){
			$('#' + proTextareaPremissegroupCheckboxId).attr('checked', false);
			$('#' + conTextareaPremissegroupCheckboxId).attr('checked', false);
		});

		// accept cookie
		$('#' + popupHowToSetPremisseGroupsOkayButton).click(function(){
			$('#' + popupHowToSetPremisseGroups).modal('hide');
			new Helper().setCookie(cookie_name);
		});
	};

	/**
	 * Updates an statement in the discussions list
	 * @param jsonData
	 */
	this.updateOfStatementInDiscussion = function (jsonData) {
		// append a row for each statement
		$('#li_' + jsonData.uid + ' input').val(jsonData.text);
		$('#li_' + jsonData.uid + ' label').text(jsonData.text);
	};

	/**
	 * Dialog based discussion modi
	 */
	this.setDisplayStyleAsDiscussion = function () {
		$('#' + islandViewContainerId).hide();
	};

	/**
	 * Some kind of pro contra list, but how?
	 */
	this.setDisplayStyleAsProContraList = function () {
		$('#' + islandViewContainerId).fadeIn('slow');
		alert('new AjaxSiteHandler().getAllArgumentsForIslandView()');
		//new AjaxSiteHandler().getAllArgumentsForIslandView();
	};

	/**
	 * Full view, full interaction range for the graph
	 */
	this.setDisplayStyleAsFullView = function () {
		$('#' + islandViewContainerId).hide();
	};

	/**
	 * Sets style attributes to default
	 */
	this.resetChangeDisplayStyleBox = function () {
		$('#' + scStyle1Id).attr('checked', true);
		$('#' + scStyle2Id).attr('checked', false);
		$('#' + scStyle3Id).attr('checked', false);
	};

	/**
	 * Sets given data as list to the issue dropdown.
	 * Also the onclick function is set
	 */
	this.setIssueList = function (jsonData){
		var li, a, current_id = '', func, topic, issueDropdownButton = $('#' + issueDropdownButtonID), issue_curr, text, pos, i, l, helper = new Helper();
		li = $('<li>');
		li.addClass('dropdown-header').text(_t(issueList));
		$('#' + issueDropdownListID).empty().append(li);

		// create an issue for each entry
		$.each(jsonData, function setIssueListEach(key, val) {
			if (key == 'current_issue') {
				current_id = val;
			} else {
				li = $('<li>');
				li.attr({id: 'issue_' + val.uid, 'issue': val.uid, 'date': val.date});
				a = $('<a>');
				a.text(val.text);
				li.append(a);
				a.click(function () {
					func = $(this).parent().attr('issue');
					topic = $('#issue_' + func + ' a').text();

					displayConfirmationDialogWithCheckbox(_t(switchDiscussion), _t(switchDiscussionText1) + ': <i>\'' + topic
						+ '\'</i> ' + _t(switchDiscussionText2), _t(keepSetting), func, true);
					// set new title and text
					issueDropdownButton.text($(this).text());
					$('#' + issueDateId).text($(this).attr('title'));
					// set inactive class
					$(this).parent().parent().children('li').each(function () {
						$(this).removeClass('disabled');
					});
					$(this).parent().addClass('disabled');
				});
				$('#' + issueDropdownListID).append(li);
			}
		});

		if (issueDropdownButton.text().length == 0 || issueDropdownButton.text().length == 15) {
			issue_curr = $('#issue_' + current_id);
			$('#' + issueDateId).text(issue_curr.attr('date'));
			text = $('#issue_' + current_id + ' a').text();
			if ($(window).width() < 1000){
				i=1;
				l = text.length;
				while (i*50 < l){
					pos = text.indexOf(' ',i*50);
					text = helper.replaceAt(text, pos, '<br>', ' ');
					i=i+1;
				}
			}
			issueDropdownButton.html(text + '&#160;&#160;&#160;<span class="caret"></span>');
			issue_curr.addClass('disabled');
		}

		// some helper
		issueDropdownButton.attr('issue', current_id);
	};
}