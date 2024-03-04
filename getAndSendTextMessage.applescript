
-- #1 REPLACE THE X's WITH THE PATH TO YOUR PYTHON SCRIPT
set pythonScriptPath to "/Users/nmestrad/Projects/automated-scripts/getTextAndNumbers.py"
-- #2 REPLACE THE X's WITH THE PATH TO WHERE YOUR PYTHON IS STORED ON YOUR COMPUTER
set shellCommand to "/Users/nmestrad/Projects/automated-scripts/.venv/bin/python " & quoted form of pythonScriptPath

-- this runs the python script and sets the return value to phoneNumbersAndMessages 
set phoneNumbersAndMessages to do shell script shellCommand
set {smsNumbers, iMessageNumbers, textMessage} to parsePhoneNumbersAndMessages(phoneNumbersAndMessages)

sendTextMessages(smsNumbers, iMessageNumbers, textMessage)

on sendTextMessages(smsNumbers, iMessageNumbers, textMessage)
	tell application "Messages"
		set smsMessageService to 1st account whose service type = SMS
        set iMessageService to 1st account whose service type = iMessage
        -- sending via iMessage
        repeat with i from 1 to count of iMessageNumbers
			set phoneNumber to item i of iMessageNumbers
            try
                send textMessage to participant phoneNumber of iMessageService
                delay 4
                log "sent message to " & phoneNumber
            on error errmsg
                log errmsg
            end try
        end repeat
        -- sending via SMS
        repeat with i from 1 to count of smsNumbers
			set phoneNumber to item i of smsNumbers
            try
                send textMessage to participant phoneNumber of smsMessageService
                delay 4
                log "sent message to " & phoneNumber
            on error errmsg
                log errmsg
            end try
        end repeat
	end tell
end sendTextMessages

on parsePhoneNumbersAndMessages(phoneNumbersAndMessages)
	set delimiter to "|**|"
	set phoneNumbersAndMessagesList to splitText(phoneNumbersAndMessages, delimiter)
    set iMessageNumbers to items 1 thru -2 of phoneNumbersAndMessagesList
    -- results is the all the android legacy numbers last sms message number and text message
    set result to item -1 of phoneNumbersAndMessagesList
    set smsNumbersAndMessage to splitText(result, "|$$|")
    set smsNumbers to items 1 thru -2 of smsNumbersAndMessage
    set textMessage to item -1 of smsNumbersAndMessage
	
	return {smsNumbers, iMessageNumbers, textMessage}
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


