import email

# https://github.com/SpamScope/mail-parser/blob/develop/mailparser/mailparser.py

wantedFields = ['Subject', 'Date', 'From', 'To', 'Message-ID', 'List-Unsubscribe', 'Return-Path', 'Content-Type',
                'Received']


def email_analyzer(filename):
    with open(filename) as file:
        result = ''
        msg = email.message_from_file(file)

        for field in wantedFields:
            for value in (msg.get_all(field) or []):
                result += field + ": " + value + '\n'
                # print(field + ": " + value)
        return result
