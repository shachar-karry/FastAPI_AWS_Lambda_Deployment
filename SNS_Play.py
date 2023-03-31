from dotenv import load_dotenv, find_dotenv
import os
import boto3

phone_book = \
{
    "shachar":"+972523370403",
    "yochay":"+972523798835",
    "gilad": "+972547824487"
}

load_dotenv(find_dotenv())

sns_client = boto3.client("sns")

#sns_client.publish(PhoneNumber="+972523370403", Message="Hello SNS")

shabat_str = \
"מזמור שיר ליום השבת, טוב להודות לה' ולזמר לשמך עליון. " \
"בכבוד השבת, נכנס לאוירה רוחנית ומפנקת של נוחות ומנוחה, ומתפנקים בקדושה ובשמחה. " \
"שבת שלום מהשבתבוט"

for id in phone_book:
    print("sending to :", id, phone_book[id])
    response = sns_client.publish(PhoneNumber=phone_book[id], Message=shabat_str)


#response = sns_client.publish(PhoneNumber="+972523370403", Message="בעזרת השם, הסמס הזה יגיע אליכם בשעה טובה וימלא את ביתכם בקדושתה של השבת המבורכת הקרובה. אמן.")

#response


