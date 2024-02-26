
-- #1 REPLACE THE X's WITH THE PATH TO YOUR PYTHON SCRIPT
set pythonScriptPath to "/Users/nmestrad/Projects/automated-scripts/getTextAndNumbers.py"
-- #2 REPLACE THE X's WITH THE PATH TO WHERE YOUR PYTHON IS STORED ON YOUR COMPUTER
set shellCommand to "/Users/nmestrad/Projects/automated-scripts/.venv/bin/python " & quoted form of pythonScriptPath

-- this runs the python script and sets the return value to phoneNumbersAndMessages 
set phoneNumbersAndMessages to do shell script shellCommand
set {phoneNumbers, textMessages} to parsePhoneNumbersAndMessages(phoneNumbersAndMessages)
sendTextMessages(phoneNumbers, textMessages)

on sendTextMessages(phoneNumbers, textMessages)
	tell application "Messages"
		set smsMessageService to 1st account whose service type = SMS
		-- set smsRecipient to participant phoneNumber of account id smsMessageType
        set iMessageService to 1st account whose service type = iMessage
		-- set iMessageRecipient to participant phoneNumber of account id iMessageType
        repeat with i from 1 to count of phoneNumbers
			set phoneNumber to item i of phoneNumbers
            try
                send textMessages to participant phoneNumber of smsMessageService
                delay 4
                log "sent message to " & phoneNumber
            on error
                try
                send textMessages to participant phoneNumber of iMessageService
                on error errmsg
                    log errmsg
                end try
            end try
        end repeat
	end tell
    -- tell application "Messages"
	-- 	set smsService to 1st account whose service type = iMessage
		
	-- 	repeat with i from 1 to count of phoneNumbers
	-- 		set phoneNumber to item i of phoneNumbers
	-- 		send textMessages to participant phoneNumber of smsService
	-- 		delay 4
	-- 	end repeat
	-- end tell
end sendTextMessages

on parsePhoneNumbersAndMessages(phoneNumbersAndMessages)
	set delimiter to "|**|"
	set phoneNumbersAndMessagesList to splitText(phoneNumbersAndMessages, delimiter)
	-- repeat with itemString in phoneNumbersAndMessagesList
	-- 	set {phoneNumber, message} to splitPhoneNumberAndMessage(itemString)
	-- 	if phoneNumber is not equal to missing value then
	-- 		set end of phoneNumbers to phoneNumber
	-- 		set end of textMessages to message
	-- 	end if
	-- end repeat
    set phoneNumbers to items 1 thru -2 of phoneNumbersAndMessagesList
    set textMessage to item -1 of phoneNumbersAndMessagesList
	
	return {phoneNumbers, textMessage}
end parsePhoneNumbersAndMessages

on splitPhoneNumberAndMessage(itemString)
	set phoneNumber to ""
	set message to ""
	
	set phoneNumberDelimiter to " "
	if itemString contains phoneNumberDelimiter then
		set phoneNumber to text 1 thru ((offset of phoneNumberDelimiter in itemString) - 1) of itemString
		set message to text ((offset of phoneNumberDelimiter in itemString) + (length of phoneNumberDelimiter)) thru -1 of itemString
	end if
	
	return {phoneNumber, message}
end splitPhoneNumberAndMessage


on splitText(inputText, delimiter)
	set text item delimiters to delimiter
	set listItems to every text item of inputText
	return listItems
end splitText


