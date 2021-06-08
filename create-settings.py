import sys

with open("settings.json","w") as file:
        file.write("{\n")
        file.write("\t\"senderEmail\":\"replace@this.mail\",\n")
        file.write("\t\"password\":\"replacePassword\",\n")
        file.write("\t\"receiverEmail\":\"replace@this.mail\"\n")
        file.write("}\n")
        file.close()