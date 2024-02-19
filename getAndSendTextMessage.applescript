
-- #1 REPLACE THE X's WITH THE PATH TO YOUR PYTHON SCRIPT
set pythonScriptPath to "/Users/nmestrad/Projects/automated-scripts/getTextAndNumbers.py"
-- #2 REPLACE THE X's WITH THE PATH TO WHERE YOUR PYTHON IS STORED ON YOUR COMPUTER
set shellCommand to "/Users/nmestrad/Projects/automated-scripts/env/bin/python " & quoted form of pythonScriptPath

-- this runs the python script and sets the return value to phoneNumbersAndMessages 
set phoneNumbersAndMessages to do shell script shellCommand
log phoneNumbersAndMessages
set {phoneNumbers, textMessages} to parsePhoneNumbersAndMessages(phoneNumbersAndMessages)
sendTextMessages(phoneNumbers, textMessages)

on sendTextMessages(phoneNumbers, textMessages)
	log {phoneNumbers, textMessages}
	tell application "Messages"
		set smsService to 1st account whose service type = iMessage
		
		repeat with i from 1 to count of phoneNumbers
			set phoneNumber to item i of phoneNumbers
			#set message to item i of textMessages
			log {phoneNumber, textMessages}
			send textMessages to participant phoneNumber of smsService
			delay 4
		end repeat
	end tell
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
    -- log phoneNumbersAndMessagesList
	
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
	-- Replace the delimiter with a unique newline character sequence
	set text item delimiters to delimiter
	set listItems to every text item of inputText
	#set text item delimiters to ASCII character 10 -- newline
	return listItems
end splitText


