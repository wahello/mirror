from enum import Enum


class Keywords(Enum):
    arguments = 'arguments'
    error = 'Error'
    iActuallyHave = 'I actually have'
    insertOneArgument = 'I have one argument:'
    insertDontCare = 'It is one argument and the system is wrongly interpreting it!'
    forgotInputRadio = 'You forgot to choose the right interpretation'
    needHelpToUnderstandStatement = 'We need your help to understand your statement!'
    setPremisegroupsIntro1 = 'You have used \'and\' in your statement: '
    setPremisegroupsIntro2 = '. There are two ways this could be interpreted. Please help us by selecting the right interpretation:'
    attack = 'You disagreed with'
    support = 'You agreed with'
    premise = 'Premise'
    because = 'Because'
    moreAbout = 'More about'
    undermine = 'It is false that'
    support1 = ''
    undercut1 = 'It is false that'
    undercut2 = 'and this is no good counter-argument'
    overbid1 = 'It is false that'
    overbid2 = 'and this is a good counter-argument'
    rebut1 = 'It is right that'
    rebut2 = ' but I have a better statement'
    oldPwdEmpty = 'Old password field is empty.'
    newPwdEmtpy = 'New password field is empty.'
    confPwdEmpty = 'Password confirmation field is empty.'
    newPwdNotEqual = 'New passwords are not equal'
    pwdsSame = 'Both entered passwords are equal.'
    oldPwdWrong = 'Your old password is wrong.'
    pwdChanged = 'Your password was changed'
    emptyName = 'Your name is empty!'
    emptyEmail = 'Your e-mail is empty!'
    emtpyContent = 'Your content is empty!'
    maliciousAntiSpam = 'Your anti-spam message is empty or wrong!'
    nonValidCSRF = 'CSRF-Token is not valid'
    name = 'Name'
    mail = 'Mail'
    phone = 'Phone'
    message = 'Message'
    messageDeleted = 'Message deleted'
    notification = 'Notification'
    notificationDeleted = 'Notification deleted'
    pwdNotEqual = 'Passwords are not equal'
    nickIsTaken = 'Nickname is taken'
    mailIsTaken = 'E-Mail is taken'
    mailNotValid = 'E-Mail is not valid'
    mailSettingsTitle = 'Enables/Disables e-mails'
    notificationSettingsTitle = 'Enables/Disables notifications'
    errorTryLateOrContant = 'An error occurred, please try again later or contact the author'
    accountWasAdded = 'Your account {} was added and you are now able to log in.'
    accountRegistration = 'D-BAS Account Registration'
    accountWasRegistered = 'Your account {} was successfully registered for this e-mail.'
    accoutErrorTryLateOrContant = 'Your account could not be added. Please try again or contact the author.'
    nicknameIs = 'Your nickname is = '
    newPwdIs = 'Your new password is = '
    dbasPwdRequest = 'D-BAS Password Request'
    antispamquestion = 'What is'
    defaultView = 'Default View'
    positions = 'Positions'
    labels = 'Labels'
    myStatements = 'My statements'
    supportsOnMyStatements = 'Supports'
    attacksOnMyStatements = 'Attacks'
    addATopic = 'Add a topic'
    pleaseEnterTopic = 'Please enter your topic here:'
    pleaseEnterShorttextForTopic = 'Please enter a short-text for your topic here:'
    pleaseSelectLanguageForTopic = 'Please select the language of the new discussion here:'
    editIssueViewChangelog = 'Edit Issues / View Changelog'
    editTitleHere = 'Please, edit the selected Title here:'
    editInfoHere = 'Please, edit the selected info here:'
    viewChangelog = 'View Changelog'
    editStatementHere = 'Please, edit the statement here:'
    save = 'Save'
    cancel = 'Cancel'
    submit = 'Submit'
    close = 'Close'
    urlSharing = 'Share your URL'
    urlSharingDescription = 'Please feel free to share this url:'
    warning = 'Warning'
    islandViewFor = 'Island View for'
    resumeHere = 'Resume here'
    aand = 'and'
    andor = 'and/or'
    addedEverything = 'Everything was added.'
    addStatementRow = 'Add another statement.'
    addTopic = 'Add a Topic'
    alreadyInserted = 'This is a duplicate and already there.'
    addPremisesRadioButtonText = 'Let me enter my reasons!'
    addArgumentsRadioButtonText = 'Let me enter my own statements!'
    argumentContainerTextIfPremises = 'You want to state your own reasons?'
    argumentContainerTextIfArguments = 'You want to state your own arguments?'
    addPremiseRadioButtonText = 'Let me enter my reason!'
    addArgumentRadioButtonText = 'Let me enter my own statement!'
    argumentContainerTextIfPremise = 'You want to state your own reason?'
    argumentContainerTextIfArgument = 'You want to state your own argument?'
    argumentContainerTextIfConclusion = 'What is your idea? What should we do?'
    argueAgainstPositionToggleButton = 'Or do you want to argue against a position? Please toggle this button:'
    argueForPositionToggleButton = 'Or do you want to argue for a position? Please toggle this button:'
    andIDoNotBelieveCounter = 'and I do not believe that this is a good counter-argument for'
    andIDoNotBelieveArgument = 'and I do not believe that this is a good argument for'
    andTheyDoNotBelieveCounter = 'and they do not believe that this is a good counter-argument for'
    andTheyDoNotBelieveArgument = 'and they do not believe that this is a good argument for'
    argumentFlaggedBecauseOfftopic = 'This argument was reported by a participant, because it probably is <strong>off topic of the discussion</strong>.'
    argumentFlaggedBecauseSpam = 'This argument was reported by a participant, because it probably is <strong>spam</strong>.'
    argumentFlaggedBecauseHarmful = 'This argument was reported by a participant, because it probably is <strong>inappropriate, harmful or abbusive</strong>.'
    argumentFlaggedBecauseOptimization = 'This argument was reported by a participant, because it probably <strong>needs optimization</strong>.'
    argumentFlaggedBecauseEdit = 'This argument was improved from a grammatical point of view.'
    alternatively = 'Alternatively'
    addArguments = 'Add arguments'
    addStatements = 'Add statements'
    addArgumentsTitle = 'Adds new arguments'
    acceptItTitle = 'Accept it...'
    acceptIt = 'Accept it...'
    asReasonFor = 'as reason for'
    argument = 'Argument'
    attackPosition = 'attack Position'
    at = 'at'
    assertion = 'assertion'
    accept = 'accept'
    agreeToThis0 = 'Nobody agrees to this statement'
    agreeToThis1 = 'agrees to this statement'
    agreeToThis2 = 'agree to this statement'
    attackedBy = 'You were attacked by'
    attackedWith = 'You\'ve attacked with'
    agreeBecause = 'I agree because '
    andIDoBelieveCounterFor = 'and I do believe that this is a counter-argument for'
    andIDoBelieveArgument = 'and I do believe that this is an argument for'
    attitudeFor = 'Attitudes for'
    alreadyFlaggedByOthers = 'This argument was already reported by others!'
    alreadyFlaggedByYou = 'You have already reported this argument!'
    breadcrumbsStart = 'Start'
    breadcrumbsChoose = 'Multiple reasons for'
    breadcrumbsJustifyStatement = 'Why do you think that'
    breadcrumbsGetPremisesForStatement = 'Get premises'
    breadcrumbsMoreAboutArgument = 'More about'
    breadcrumbsReplyForPremisegroup = 'Reply for group'
    breadcrumbsReplyForResponseOfConfrontation = 'Justification of'
    breadcrumbsReplyForArgument = 'Reply for argument'
    butIDoNotBelieveCounterFor = 'but I do not believe that this is a counter-argument for'
    butIDoNotBelieveArgumentFor = 'but I do not believe that this is a argument for'
    butIDoNotBelieveCounter = 'but I do not believe that this is a counter-argument for'
    butIDoNotBelieveArgument = 'but I do not believe that this is a argument for'
    butIDoNotBelieveReasonForReject = 'but I do not believe that this is a reason for reject'
    butTheyDoNotBelieveCounter = 'but they do not believe that this is a good counter-argument for'
    butSheDoesNotBelieveCounter = 'but she does not believe that this is a good counter-argument for'
    butHeDoesNotBelieveCounter = 'but he do not believe that this is a good counter-argument for'
    butTheyDoNotBelieveArgument = 'but they do not believe that this is a good argument for'
    butSheDoesNotBelieveArgument = 'but she does not believe that this is a good argument for'
    butHeDoesNotBelieveArgument = 'but he does not believe that this is a good argument for'
    butOtherParticipantsDontHaveOpinionRegardingYourOpinion = 'but other participants do not have any opinion regarding your selection'
    butOtherParticipantsDontHaveArgument = 'but other participants do not have any argument for that.'
    butOtherParticipantsDontHaveCounterArgument = 'but other participants do not have any counter argument for that.'
    butWhich = 'but which one'
    but = 'but'
    butThenYouCounteredWith = 'But then you did not agree with this because'
    butYouCounteredWith = 'You did not agree with this because'
    butYouAgreedWith = 'And you agreed with this because'
    canYouGiveAReason = 'Can you give a reason?'
    canYouGiveAReasonFor = 'Can you give a reason for'
    canYouGiveACounter = 'Can you give a counter-argument?'
    canYouGiveACounterArgumentWhy1 = 'Can you give a counter-argument, why are you against'
    canYouGiveACounterArgumentWhy2 = '?'
    canYouGiveAReasonForThat = 'Can you give a reason for that?'
    clickHereForRegistration = 'Click <a data-toggle="modal" data-target="#popup-login" title="Login" data-href="login" >here</a> for log in or registration!'
    clickForMore = 'Click for more!'
    countOfArguments = 'Count of arguments'
    countOfPosts = 'Count of posts'
    confirmation = 'Confirmation'
    contact = 'Contact'
    contactSubmit = 'Submit your Message'
    confirmTranslation = 'If you change the language, your process on this page will be lost and you have to restart the discussion!'
    correctionsSet = 'Your correction was set.'
    checkFirstname = 'Better check your first name, because the input is empty!'
    checkLastname = 'Better check your last name, because the input is empty!'
    checkNickname = 'Better check your nickname, because the input is empty!'
    checkEmail = 'Better check your email, because the input is empty!'
    checkPassword = 'Better check your password, because the input is empty!'
    checkConfirmation = 'Better check the confirmation of your password, because the input is empty!'
    completeView = 'Complete View'
    completeViewTitle = 'Shows the complete graph'
    checkPasswordConfirm = 'Better check your passwords, because they are not equal!'
    clickToChoose = 'Click to choose'
    clearStatistics = 'Clear Statistics'
    congratulation = 'Congratulation!'
    currentDiscussion = 'Current discussion is about'
    description_undermine = 'This statement attacks the premise.'
    description_support = 'This statement supports the premise.'
    description_undercut = 'This statement attacks the justification (undercut). You do not believe that the premise justifies the conclusion.'
    description_overbid = 'This statement supports the justification (overbid). You do believe that the premise justifies the conclusion.'
    description_rebut = 'This statement is against the conclusion itself.'
    description_no_opinion = 'You just have no opinion regarding the confrontation or you just want to skip this.'
    decisionIndex7 = 'Decision Index - Last 7 Days'
    decisionIndex30 = 'Decision Index - Last 30 Days'
    decisionIndex7Info = 'Count of made decision (due to clicks in a discussion) in the last 7 days'
    decisionIndex30Info = 'Count of made decision (due to clicks in a discussion) in the last 30 days'
    dateString = 'Date'
    deleteTrack = 'Delete track'
    deleteStatement = 'Delete statement'
    disassociateStatement = 'Disassociate from statement'
    deleteHistory = 'Delete history'
    delete = 'Delete'
    disagreeBecause = 'I disagree because '
    dataRemoved = 'Data was successfully removed.'
    didYouMean = 'Top10 statements, which you probably could mean:'
    dialogView = 'Dialog View'
    dialogViewTitle = 'Show the dialog View'
    displayControlDialogGuidedTitle = 'Dialog View'
    displayControlDialogGuidedBody = 'You will never see something like an argumentation map, because the systems seems to be like a dynamic and generic.'
    displayControlDialogIslandTitle = 'Island View'
    displayControlDialogIslandBody = 'Okay, you want to see more as, but not everything. Therefore the island view will present you a list of every connected statement for an specific statement.'
    displayControlDialogExpertTitle = 'Expert View'
    displayControlDialogExpertBody = 'So, you think you are an expert? Okay, you can have a view of the complete argumentation map'
    displayControlDialogGraphTitle = 'Graph-View'
    displayControlDialogGraphBody = 'Presentation of the discusion as graph.'
    discussionEnd = 'The discussion ends here.'
    discussionCongratulationEnd = 'The discussion ends here, because there is no other counter argument at the moment.'
    discussionEndLinkTextLoggedIn = 'Are you looking for things to do? Take a look at the <a id="discussionEndReview">review section</a>. Alternatively you can restart the discussion with the button above.'
    discussionEndLinkTextNotLoggedIn = 'Are you looking for things to do? <a  data-href="login" data-toggle="modal" data-target="#popup-login" title="Login">Login</a> and take a look at the <a id="discussionEndReview">review section</a>. Alternatively you can restart the discussion with the button above.'
    discussionInfoTooltip1 = 'The discussion was started'
    discussionInfoTooltip2 = 'and already has'
    discussionInfoTooltip3sg = 'argument.'
    discussionInfoTooltip3pl = 'arguments.'
    disagreeToThis0 = 'Nobody disagree to this statement'
    disagreeToThis1 = 'disagrees to this statement'
    disagreeToThis2 = 'disagree to this statement'
    duplicate = 'Duplikat'
    duplicateDialog = 'This textversion is deprecated, because it was already edited to this version.\nDo you want to set this version as the current one once again?'
    doesNotHold = 'does not hold'
    isNotRight = 'does not hold'
    isNoGoodJustification = 'is not a good justification'
    doNotHesitateToContact = 'Do not hesitate to <span style="cursor: pointer;" id="contact-on-error"><strong>contact us (click here)</strong></span>'
    doesJustify = 'does justify that'
    doesNotJustify = 'does not justify that'
    doYouWantToEnterYourStatements = 'Do you want to enter your statement(s)?'
    dataNowLocked = 'You locked the data.'
    dataUnlocked = 'Data unlocked!'
    dataAlreadyLockedByYou = 'You are already editing data. Please finish your work first!'
    dataAlreadyLockedByOthers = 'Sorry, this data edited by other participants.'
    earlierYouArguedThat = 'Earlier you argued that'
    editIndex = 'Edit Index - Last 30 Tage'
    editIndexInfo = 'Count of Edits'
    euCookiePopupTitle = 'This website is using cookies and Piwik.'
    euCookiePopupText = 'We use them to give you the best experience. If you continue using our website, we\'ll assume that you are happy to receive all cookies on this website and being tracked for academic purpose. All tracked data are saved anonymously with reduced masked IP-addresses.'
    euCookiePopoupButton1 = 'Continue'
    euCookiePopoupButton2 = 'Learn&nbsp;more'
    empty_news_input = 'News title or text is empty or too short!'
    empty_notification_input = 'Notification title or text is empty or too short!'
    email = 'E-Mail'
    emailWasSent = 'E-Mail was sent.'
    emailWasNotSent = 'E-Mail was not sent.'
    emailUnknown = 'The given mail address is unknown.'
    emailBodyText = 'This is an automatically generated mail by D-BAS {}.\nFor contact please write a mail to krauthoff@cs.uni-duesseldorf.de\nThis system is part of a doctoral thesis and currently in a beta-phase.'
    emailArgumentAddTitle = 'D-BAS Information about an Argument'
    emailArgumentAddBody = 'New statements were added to your argument. Have a look at:'
    exampleName = 'example: Tobias Krauthoff'
    exampleMail = 'example: krauthoff@cs.uni-duesseldorf.de'
    examplePhone = 'example: +49 (0)211 81-13461'
    exampleMessage = 'example: I\'d like to say good job!'
    exampleNickname = 'example: Democrator'
    examplePassword = 'example: ********'
    exampleNicknameLdap = 'example: tokra100'
    exampleFirstname = 'example: Tobias'
    exampleLastname = 'example: Krauthoff'
    exampleStatement = 'Please enter the source here'
    exampleSource = 'Please enter the cite here'
    error_code = 'Error code'
    edit = 'Edit'
    editTitle = 'Edit statement'
    feelFreeToLogin = 'If you want to proceed, please feel free to <a  data-href="login" data-toggle="modal" data-target="#popup-login" title="Login">login</a>.'
    forText = 'for'
    forThat = 'accept that'
    firstConclusionRadioButtonText = 'Let me enter my idea!'
    firstArgumentRadioButtonText = 'Let me enter my own statement(s)!'
    feelFreeToShareUrl = 'Please feel free to share this url'
    fetchLongUrl = 'Long URL'
    fetchShortUrl = 'Short URL'
    forgotPassword = 'Forgot Password'
    firstOneInformationText = 'You are the first one, who is interested in: '
    firstOneInformationTextM = 'You are the first one, who is interested in:  '
    firstOneInformationTextF = 'You are the first one, who is interested in:   '
    firstOneReason = 'You are the first one with this argument, please give a reason.'
    firstOneReasonM = 'You are the first one with this argument, please give a reason. '
    firstOneReasonF = 'You are the first one with this argument, please give a reason.  '
    firstPositionText = 'You are the first one in this discussion!'
    firstPositionTextM = 'You are the first one in this discussion! '
    firstPositionTextF = 'You are the first one in this discussion!  '
    firstPremiseText1 = 'You are the first one, who said that'
    firstPremiseText1M = 'You are the first one, who said that '
    firstPremiseText1F = 'You are the first one, who said that  '
    firstPremiseText2 = 'Please enter your reason for your statement.'
    firstname = 'First name'
    fillLine = 'Please, fill this this line with your report'
    finishTitle = 'Leave the discussion!'
    fromm = 'from'
    gender = 'Gender'
    goBack = 'Click to go back'
    goHome = 'Go home'
    goStepBack = 'Go one step back'
    generateSecurePassword = 'Generate secure password'
    goodPointTakeMeBackButtonText = 'I agree, that is a good argument! Take me one step back.'
    group_uid = 'Group'
    goBackToTheDiscussion = 'Go back to the discussion'
    goForward = 'Click to go forward'
    haveALookAt = 'Hey, please have a look at '
    hidePasswordRequest = 'Hide Password Request'
    hideGenerator = 'Hide Generator'
    hold = 'hold'
    howeverIHaveMuchStrongerArgumentRejectingThat = 'However, I have a much stronger argument for reject that'
    howeverIHaveMuchStrongerArgumentAcceptingThat = 'However, I have a much stronger argument for accept that'
    howeverIHaveMuchStrongerArgument = 'However, I have a much stronger argument to'
    howeverIHaveEvenStrongerArgumentRejecting = 'However, I have an even stronger argument for reject that'
    howeverIHaveEvenStrongerArgumentAccepting = 'However, I have an even stronger argument for accept that'
    imprint = 'Imprint'
    iAgreeWithInColor = 'I <span class=\'text-success\'>agree</span>'
    iAgreeWith = 'I agree '
    iDisagreeWithInColor = 'I <span class=\'text-danger\'>disagree</span>'
    iDisagreeWith = 'I disagree'
    iDoNotKnow = 'I do not know'
    iDoNotKnowInColor = 'I <span class=\'text-info\'>do not know</span>'
    iHaveNoOpinionYet = 'I have no opinion yet about'
    iHaveNoOpinion = 'I have no opinion'
    iHaveNoOpinionYetInColor = 'I have <span class=\'text-info\'>no opinion yet</span>, show me an argument'
    informationForExperts = 'Information for experts'
    internalFailureWhileDeletingTrack = 'Internal failure, please try again or did you have deleted your track recently?'
    internalFailureWhileDeletingHistory = 'Internal failure, please try again or did you have deleted your history recently?'
    internalError = '<strong>Internal Error:</strong> Maybe the server is offline.'
    internalKeyError = 'Internal error while reading input data.'
    issueList = 'Topics'
    islandViewHeaderText = 'These are all arguments for = '
    islandView = 'Island View'
    islandViewTitle = 'Shows the island View'
    irrelevant = 'Irrelevant'
    itIsTrueThat = 'it is true that'
    itIsTrue1 = ' '
    itIsTrue2 = ' is true'
    itIsFalseThat = 'it is false that'
    itIsFalse1 = '  '
    itIsFalse2 = 'is false'
    itTrueIsThat = 'it is true that '
    itFalseIsThat = 'it is false that '
    isFalse = 'is false '
    isNotAGoodIdea = 'is not a good idea'
    isNotAGoodIdeaInColor = '<span class=\'text-danger\'>is not a good idea</span>'
    isTrue = 'is true'
    areTrue = 'are true'
    initialPosition = 'Initial Position'
    initialPositionSupport = 'What is your initial position you are supporting?'
    initialPositionAttack = 'What is your initial position you want to attack?'
    initialPositionInterest = 'I want to talk about the position that ...'  # What is the initial position you are interested in?'
    invalidEmail = 'Your mail is invalid!'
    iAcceptCounter = 'and I do accept that this is a counter-argument for'
    iAcceptArgument = 'and I do accept that this is an argument for'
    iAcceptCounterThat = 'and I do accept that this is a counter-argument for'
    iAcceptArgumentThat = 'and I do accept that this is an argument for'
    iHaveMuchStrongerArgumentRejecting = 'I have a much stronger argument for reject that'
    iHaveEvenStrongerArgumentRejecting = 'I have an even stronger argument for reject that'
    iHaveMuchStrongerArgumentAccepting = 'I have a much stronger argument for accept that'
    iHaveEvenStrongerArgumentAccepting = 'I have an even stronger argument for accept that'
    iNoOpinion = 'I have no opinion regarding'
    interestingOnDBAS = 'Interesting discussion on DBAS'
    inputEmpty = 'Input is empty!'
    informationForStatements = 'Information of the statements'
    relativePopularityOfStatements = 'Relative popularity of Statements'
    jumpAnswer0 = 'Right, I support the {} and accept the {}.'
    jumpAnswer1 = 'Right, I support the {}, but I want to add my own {}.'
    jumpAnswer2 = 'Right, I support the {}, but the {} does not support it.'
    jumpAnswer3 = 'Wrong, the {} is false.'
    jumpAnswer4 = 'Wrong, the {} does not hold.'
    justLookDontTouch = 'Just look, do not touch anything!'
    keyword = 'Keyword'
    keywordStart = 'Start'
    keywordChooseActionForStatement = 'Choosing attitude'
    keywordGetPremisesForStatement = 'Getting premises'
    keywordMoreAboutArgument = 'More about'
    keywordReplyForPremisegroup = 'Reply for argument'
    keywordReplyForResponseOfConfrontation = 'Justification of'
    keywordReplyForArgument = 'Confrontation'
    keepSetting = 'Keep this'
    holds = 'holds'
    holdsInColor = '<span class=\'text-success\'>holds</span>'
    hideAllUsers = 'Hide all users'
    hideAllAttacks = 'Hide all attacks'
    letMeExplain = 'Let me explain it this way'
    levenshteinDistance = 'Levenshtein-Distance'
    languageCouldNotBeSwitched = 'Unfortunately, the language could not be switched'
    last_action = 'Last Action'
    last_login = 'Last Login'
    login = 'Login'
    logfile = 'Logfile for'
    letsGo = 'Click here to start now!'
    letsGoBack = 'Let\'s go back!'
    letsGoHome = 'Let\'s go home!'
    langNotFound = 'Language not found'
    latestNewsFromDiscussion = 'Latest news about actions in the discussion'
    latestNewsFromDBAS = 'Latest news about D-BAS, a Dialog-Based Argumentation System'
    more = 'More'
    medium = 'medium'
    minLength = 'Minimal length'
    myArgument = 'my argument'
    next = 'Next Entry'
    now = 'Now'
    nowYouSayThat = 'Now you say that'
    newNotification = 'You got a new notification.'
    newMention = 'You are mentioned in a contribution.'
    newPremiseRadioButtonText = 'None of the above! Let me state my own reason!'
    newPremisesRadioButtonText = 'None of the above! Let me state my own reason(s)!'
    newPremiseRadioButtonTextAsFirstOne = 'Let me state my own reason!'
    newPremisesRadioButtonTextAsFirstOne = 'Let me state my own reason(s)!'
    newStatementRadioButtonTextAsFirstOne = 'Let me state my own statement!'
    newStatementsRadioButtonTextAsFirstOne = 'Let me state my own statement(s)!'
    newConclusionRadioButtonText = 'Neither of the above, I have a different idea!'
    newConclusionRadioButtonTextNewIdea = 'I have a new idea!'
    newsAboutDbas = 'News about D-BAS'
    nickname = 'Nickname'
    noOtherAttack = 'The system has no other counter-argument'
    noIslandView = 'Could not fetch data for the island view. Sorry!'
    noCorrections = 'No corrections for the given statement could be fetched.'
    noCorrectionsSet = 'Correction could not be set, because your user was not fount in the database. Are you currently logged in?'
    noDecisionDone = 'No decision was done.'
    notInsertedErrorBecauseEmpty = 'Your idea was not inserted, because your text is too short or empty.'
    notInsertedErrorBecauseDuplicate = 'Your idea was not inserted, because your idea is a duplicate.'
    notInsertedErrorBecauseUnknown = 'Your idea was not inserted due to an unknown error.'
    notInsertedErrorBecauseInternal = 'Your idea was not inserted due to an internal error.'
    noEntries = 'No entries'
    noTrackedData = 'No data was tracked.'
    number = 'No'
    note = 'Note'
    no_entry = 'No entry'
    no_arguments = 'No arguments for this opinion'
    noRights = 'You have no rights for this action!'
    notLoggedIn = 'You are not logged in.'
    on = 'On'
    of = 'of'
    off = 'Off'
    opinion_his = 'his opinion'
    opinion_her = 'her opinion'
    opinion = 'the opinion'
    onlyOneItem = 'If you want to state a new reason, please click here to log in.'
    onlyOneItemWithLink = 'If you want to state a new reason, please click <a data-href="login" data-toggle="modal" data-target="#popup-login" title="Login">here</a> to log in.'
    unfortunatelyOnlyOneItem = 'Unfortunately you only have one option to choose. If you want to state a new reason, please click <a data-href="login" data-toggle="modal" data-target="#popup-login" title="Login">here</a> to log in.'
    otherParticipantsConvincedYouThat = 'Other participants convinced you that'
    otherParticipantsThinkThat = 'Other participants think that'
    otherParticipantsAgreeThat = 'Other participants agree that'
    thinkThat = 'think that'
    agreeThat = 'agree that'
    thinksThat = 'thinks that'
    agreesThat = 'agrees that'
    otherParticipantsDontHaveOpinion = 'Other participants do not have any opinion regarding'
    otherParticipantsDontHaveOpinionRegaringYourSelection = 'Other participants do not have any opinion regarding your selection'
    otherParticipantsDontHaveCounterForThat = 'Other participants do not have any counter-argument for that'
    otherParticipantsDontHaveNewCounterForThat = 'Other participants do not have any new counter-argument for that. You already have seen all other counter-arguments.'
    otherParticipantsDontHaveCounter = 'Other participants do not have any counter-argument for '
    otherParticipantsDontHaveArgument = 'Other participants do not have any argument for '
    otherParticipantsAcceptBut = 'Other participants accept your argument, but'
    otherParticipantDisagreeThat = 'Other participants disagree that '
    otherUsersClaimStrongerArgumentS = 'claims to have a stronger statement to {}'
    otherUsersClaimStrongerArgumentP = 'Other participants claim to have a stronger statement to {}'
    claimsStrongerArgumentRejecting = 'claims to have a stronger statement for reject'
    claimsStrongerArgumentAccepting = 'claims to have a stronger statement for accept'
    otherUsersHaveCounterArgument = 'Other participants have the counter-argument that'
    otherUsersSaidThat = 'Other participants said that'
    opinionBarometer = 'Opinion Barometer'
    pleaseAddYourSuggestion = 'Please add your suggestion!'
    premiseGroup = 'PremiseGroup'
    previous = 'Previous Entry'
    publicNickTitle = 'Enables/Disables the real nickname on your public page.'
    passwordSubmit = 'Change Password'
    preferedLangTitle = 'Preferred language for all notifications/mails'
    priv_access_opti_queue = 'Access to the optimization queue'
    priv_access_del_queue = 'Access to the delete queue'
    priv_access_edit_queue = 'Access to the edit queue'
    priv_history_queue = 'Access to all reviews of the past'
    publications = 'Publications'
    queueDelete = 'Deletes'
    queueOptimization = 'Optimizations'
    queueEdit = 'Edits'
    queueHistory = 'History'
    queueOngoing = 'Ongoing'
    myPosition = 'my point of view'
    myPositionGenitiv = 'my point of view '
    the_der = 'the'
    the_die = 'the '
    the_das = 'the  '
    reference = 'Reference'
    registered = 'Registered'
    restartDiscussion = 'Restart Discussion'
    restartDiscussionTitle = 'Restart Discussion'
    restartOnError = 'Please try to reload this page or restart the discussion, if reloading does not fix the problem.'
    recipient = 'Recipient'
    recipientNotFound = 'Recipient not found!'
    report = 'Report'
    reportStatement = 'Report statement'
    reportArgument = 'Report argument'
    review = 'Review'
    review_history = 'Review History'
    review_ongoing = 'Current Reviews'
    right = 'Right'
    reason = 'Reason'
    requestTrack = 'Request track'
    refreshTrack = 'Refresh track'
    requestHistory = 'Request history'
    refreshHistory = 'Refresh history'
    requestFailed = 'Request failed'
    reject = 'reject'
    remStatementRow = 'Removes this row.'
    reaction = 'Reactions'
    attitudesOfOpinions = 'Attitudes of the Opinions'
    reactionFor = 'Reactions for'
    agreeVsDisagree = 'Agree vs. Disagree'
    rep_reason_first_argument_click = 'You choose your first argument.'
    rep_reason_first_confrontation = 'You survived your first confrontation'
    rep_reason_first_position = 'You entered a new position for the first time'
    rep_reason_first_justification = 'You entered a new justification for the first time'
    rep_reason_first_new_argument = 'You entered a new argument for the first time'
    rep_reason_new_statement = 'For any argument you entered after your first one'
    rep_reason_success_flag = 'You set your first flag'
    rep_reason_success_edit = 'You send your first edit'
    rep_reason_bad_flag = 'You misused the flag function'
    rep_reason_bad_edit = 'You made a bad edit'

    reaction_text_undermine = 'reaction_text_undermine_german_only'
    reaction_text_support = 'reaction_text_support_german_only'
    reaction_text_undercut = 'reaction_text_undercut_german_only'
    reaction_text_undercut_for_dont_know = 'reaction_text_undercut_for_dont_know_german_only'
    reaction_text_rebut = 'reaction_text_rebut_german_only'
    reaction_text_rebut_for_dont_know = 'reaction_text_rebut_for_dont_know_german_only'

    questionTitle = 'Get more information about the statement!'
    saveMyStatement = 'Save my Statement!'
    selectStatement = 'Please select a statement!'
    showAllUsers = 'Show all users'
    showAllArguments = 'Show all arguments'
    showAllArgumentsTitle = 'Show all arguments, done by users'
    showAllUsersTitle = 'Show all users, which are registered'
    supportPosition = 'support position'
    supportsNot = 'does not support'
    isupport = 'I support'
    strength = 'Strength'
    strong = 'strong'

    strongerStatementForF = 'but she claims to have a stronger statement for '
    strongerStatementForM = 'but he claims to have a stronger statement for '
    strongerStatementForP = 'but they claim to have a stronger statement for '
    accepting = 'accepting'
    rejecting = 'rejecting'
    strongerStatementEnd = '   '

    someoneArgued = 'Someone argued that'
    soYouEnteredMultipleReasons = 'So you entered multiple reasons'
    soYourOpinionIsThat = 'So your opinion is that'
    soYouWantToArgueAgainst = 'So you want to counter-argue against'
    shortenedBy = 'which was shortened with'
    shareUrl = 'Share Link'
    showMeAnotherArgument = 'Show me another argument'
    soThatOtherParticipantsDontHaveOpinionRegardingYourOpinion = 'so that participants do not have any opinion regarding your selection'
    switchDiscussion = 'Change the discussion\'s topic'
    switchDiscussionTitle = 'Switch Discussion'
    switchDiscussionText1 = 'If you accept, you will change the topic of the discussion to'
    switchDiscussionText2 = 'and the discussion will be restarted.'
    switchLanguage = 'Switch Language'
    statement = 'Statement'
    statementAdded = 'Statement was added'
    statementIsAbout = 'Statement is about'
    settings = 'Settings'
    senderReceiverSame = 'Sender and reveicer are equal'
    argumentAdded = 'Argument was added'
    statementAddedMessageContent = 'Hey, someone has added his/her opinion regarding your argument!'
    argumentAddedMessageContent = 'Hey, someone has added his/her argument regarding your argument!'
    statementIndex = 'Statement Index - Last 30 Days'
    statementIndexInfo = 'Count of added Statements'
    sureThat = 'I\'m reasonably sure that '
    surname = 'Surname'
    myStatement = 'my statement'
    showMeAnArgumentFor = 'Show me an argument for'
    textAreaReasonHintText = 'Please use a new text area for every reason, write short and clear!'
    theCounterArgument = 'the counter-argument'
    therefore = 'Therefore'
    thinkWeShould = 'I think we should '
    track = 'Track'
    this = 'this'
    textversionChangedTopic = 'Statement was edited'
    textversionChangedContent = 'Your original statement was edited by'
    to = 'to'
    history = 'History'
    topicString = 'Topic'
    text = 'Text'
    theySay = 'They say'
    heSays = 'He says'
    sheSays = 'She says'
    theyThink = 'They think'
    heThinks = 'he thinks'
    sheThinks = 'she thinks'
    thisIsACopyOfMail = 'This is a copy of your mail'
    thisConfrontationIs = 'This confrontation is a'
    thisArgument = 'this argument'

    theirArgument = 'their argument'
    hisArgument = 'his argument'
    herArgument = 'her argument'
    theirStatement = 'their statement'
    hisStatement = 'his statement'
    herStatement = 'her statement'
    theirAssertion = 'their assertion'
    herAssertion = 'her assertion'
    hisAssertion = 'his assertion'
    theirPosition = 'their point of view'
    hisPosition = 'his point of view'
    herPosition = 'her point of view'
    theirReason = 'their reason'
    herReason = 'her reason'
    herReasonGenitiv = 'her reason '
    hisReason = 'his reason'

    textChange = 'Some statement of yours was edited.'
    thxForFlagText = 'Thanks for reporting, we will have a look at it!'
    veryweak = 'very weak'
    wantToStateNewPosition = 'If you want to state a new position, please click here to log in.'
    weak = 'weak'
    wrong = 'Wrong'
    where = 'Where'
    wouldYourShareArgument = 'Would you share your argument?'
    whatDoYouThinkAbout = 'What do you think about'
    whatDoYouThinkOf = 'What do you think of'
    whatDoYouThinkAboutThat = 'What do you think about that'
    whatIsYourIdea = 'What is your idea / opinion? What should we do?'
    whatIsYourMostImportantReasonFor = 'What is your most important reason for'
    whatIsYourMostImportantReasonWhyFor = 'What is your most important reason why'
    whatIsYourMostImportantReasonWhyAgainst = 'What is your most important reason why   '
    whatIsYourMostImportantReasonWhyForInColor = 'What is your most important reason why  '
    whatIsYourMostImportantReasonWhyAgainstInColor = 'What is your most important reason why '
    whyDoYouThinkThat = 'Why do you think that'
    wrongURL = 'Your URL seems to be wrong.'
    whyAreYouDisagreeingWith = 'Why are you disagreeing with'
    whyAreYouAgreeingWith = 'Why are you agreeing with'
    whyAreYouDisagreeingWithInColor = 'Why are you <span class=\'text-danger\'>disagreeing</span> with'
    whyAreYouAgreeingWithInColor = 'Why are you <span class=\'text-success\'>agreeing</span> with'
    whyAreYouDisagreeingWithThat = 'Why are you disagreeing with that?'
    youMadeA = 'You made a'
    youMadeAn = 'You made an'
    relation_undermine = 'is a counter-argument for'
    relation_support = 'is a reason for'
    relation_undercut = 'is a counter-argument for'
    relation_overbid = 'is a reason for'
    relation_rebut = 'is a counter-argument for'
    uid = 'ID'
    unfortunatelyNoMoreArgument = 'Unfortunately there are no more arguments about'
    userPasswordNotMatch = 'User / Password do not match'
    userOptions = 'Users Options'
    userNotFound = 'User not found'
    userIsNotAuthorOfStatement = 'You are not the author of this statement'
    userIsNotAuthorOfArgument = 'You are not the author of this argument'
    voteCountTextFirst = 'You are the first one with this opinion'
    voteCountTextMayBeFirst = 'You would be the first one with this opinion'
    voteCountTextOneOther = 'One other participant with this opinion'
    voteCountTextMore = 'more participants with this opinion'
    voteCountTextOneMore = ' participant with this opinion'
    visitDeleteQueue = 'Visit the delete queue of D-BAS.'
    visitDeleteQueueLimitation = 'You need at least {} reputation points to review deletes.'
    visitEditQueue = 'Visit the edit queue of D-BAS.'
    visitEditQueueLimitation = 'You need at least {} reputation points to review edits.'
    visitOptimizationQueue = 'Visit the optimization queue of D-BAS.'
    visitOptimizationQueueLimitation = 'You need at least {} reputation points to review optimizations.'
    visitHistoryQueue = 'Visit the history of reviews of D-BAS.'
    visitHistoryQueueLimitation = 'You need at least {} reputation points to have a look into the past.'
    visitOngoingQueue = 'Visit the current ongoing reviews of D-BAS.'
    welcome = 'Welcome'
    welcomeMessage = 'Welcome to the novel dialog-based argumentation system.<br>We hope you enjoy using this system and happy arguing!'
    youAreInterestedIn = 'You are interested in'
    youAgreeWith = 'You agree with'
    youAgreeWithThatNow = 'Now you agree that'
    youDisagreeWith = 'You disagree with'
    youSaidThat = 'You said that'
    youUsedThisEarlier = 'You used this earlier'
    youRejectedThisEarlier = 'You rejected this earlier'
    youHaveMuchStrongerArgumentForAccepting = 'You have a much stronger argument for accept'
    youHaveMuchStrongerArgumentForRejecting = 'You have a much stronger argument for reject'
    # insertDontCare = 'I don’t care about this, leave me alone and take my statement as it is!'
    youAreAbleToReviewNow = 'You are now able to visit the review section.'
    youArgue = 'You argue about'

    @staticmethod
    def get_key_by_string(string):
        """
        Returns a key by his name

        :raises KeyError if the key is not in the enumeration

        :param string: The name of the key
        :return: The key
        """
        for key in Keywords:
            if key.name == string:
                return key

        raise KeyError('Invalid key: {}'.format(string))
