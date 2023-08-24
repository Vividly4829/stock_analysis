import openpyxl
import re

def extract_emails(email_list):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, email_list)
    return emails

# Load the workbook and define the sheet
wb = openpyxl.load_workbook('gid_list_may.xlsx')

# Define the sheet
sheet = wb['Sheet1']

# loop through each row and add it to a list

mail_addresses = 'Aasebø, Ove <ove.aaseboe@siemens-energy.com>; Abdul Ameer, Wisam Fadhel <wisam.f.ameer@siemens-energy.com>; Ånderå, Andreas Sortland <andreas.andera@siemens-energy.com>; Andreev, Alexey Gennadievich <alexey.andreev@siemens-energy.com>; Anthun, Tormod <tormod.anthun@siemens-energy.com>; Bergtun, Inge Martin <inge.m.bergtun@siemens-energy.com>; Bjelland, Torbjørn <torbjoern.bjelland@siemens-energy.com>; Bjørnevik, Silje <silje.bjoernevik@siemens-energy.com>; Bø, Svein Tore <sveintore.bo@siemens-energy.com>; Borgen, Ann-Helen <ann-helen.borgen@siemens-energy.com>; Eastoe, Andrew Robert <andrew.r.eastoe@siemens-energy.com>; Eikemo, Katrine Sortland <katrine.eikemo@siemens-energy.com>; Engevik, Fredrik Lie <fredrik.engevik@siemens-energy.com>; Ersland, Gunnar <gunnar.ersland@siemens-energy.com>; Espeland, Ruben <ruben.espeland@siemens-energy.com>; Fadeeva, Veronika <veronika.fadeeva@siemens-energy.com>; Fjellheim, Cato <cato.fjellheim@siemens-energy.com>; Folgerø-Holm, Jan Inge <jan.i.folgeroe-holm@siemens-energy.com>; Furdal, Håkon <haakon.furdal@siemens-energy.com>; Furnes, Eli <eli.furnes@siemens-energy.com>; Fylkesnes, Anjerd Mjånes <anjerd.fylkesnes@siemens-energy.com>; Gåsland, Simen Sæverud <simen.gaasland@siemens-energy.com>; Habbestad, Julie Sakseide <julie-sakseide.habbestad@siemens-energy.com>; Haldorsen, Kjetil <kjetil.haldorsen@siemens-energy.com>; Haldorsen, Morten <morten.haldorsen@siemens-energy.com>; Haldorsen, Tore <tore.haldorsen@siemens-energy.com>; Halleraker, Arne <arne.halleraker@siemens-energy.com>; Halleraker, Cathrine <cathrine.halleraker@siemens-energy.com>; Halleraker, Roger <roger.halleraker@siemens-energy.com>; Halleraker, Steffen <steffen.halleraker@siemens-energy.com>; Hammersland, Arne <arne.hammersland@siemens-energy.com>; Hauge, Andreas <andreas.hauge@siemens-energy.com>; Havn, Andreas <andreas.havn@siemens-energy.com>; Hidle, Daniel <daniel.hidle@siemens-energy.com>; Hollund, Bjørn Vidar <bjoern.hollund@siemens-energy.com>; Hovland, Jon Morten <jon.hovland@siemens-energy.com>; Hukset, Einar Ove <einar.o.hukset@siemens-energy.com>; Husa, Camilla <camilla.husa@siemens-energy.com>; Husa, Torbjørn <torbjoern.husa@siemens-energy.com>; Hystad, Arild <arild.hystad@siemens-energy.com>; Innvær, Johannes <johannes.innvaer@siemens-energy.com>; Innvær, Kåre <kaare.innvaer@siemens-energy.com>; Innvær, Nils Gunnar <nils.innvaer@siemens-energy.com>; Katla, Kristine Gilje <kristine.katla@siemens-energy.com>; Katla, Martin <martin.katla@siemens-energy.com>; Kloven, Stine <stine.kloven@siemens-energy.com>; Knutsson, Hans <hans.knutsson@siemens-energy.com>; Koch, Torill <torill.koch@siemens-energy.com>; Kråkenes, Thomas Nordhus <thomas.krakenes@siemens-energy.com>; Kristiansen, Lars Kristian <lars.kristiansen@siemens-energy.com>; Kvernenes, Daniel <daniel.kvernenes@siemens-energy.com>; Kvernenes, Tobias <tobias.kvernenes@siemens-energy.com>; Larsen, Christine <christine.a.larsen@siemens-energy.com>; Lidal, Laurits <laurits.lidal@siemens-energy.com>; Lønning, Amund <amund.loenning@siemens-energy.com>; Mæland, Sigbjørn <sigbjoern.maeland@siemens-energy.com>; Mathiesen, Svein Magne <svein.m.mathiesen@siemens-energy.com>; Matthiesen, Are <are.matthiesen@siemens-energy.com>; Mehammer, Frida T <frida.t.mehammer@siemens-energy.com>; Meland, Bjørn Åge <bjoern.a.meland@siemens-energy.com>; Meling, Vibecke <vibecke.meling@siemens-energy.com>; Mellesdal, Øyvind Espeland <oeyvind.mellesdal@siemens-energy.com>; Michaelsen, Petter <petter.michaelsen@siemens-energy.com>; Moss, Linda <linda.moss@siemens-energy.com>; Nordtun, Renate <renate.nordtun@siemens-energy.com>; Norum, Ramona Isaksen <ramona.norum@siemens-energy.com>; Nysæther, Marita <marita.nysaether@siemens-energy.com>; Olsen, Per Johan <perjohan.olsen@siemens-energy.com>; Onarheim, Bjørn Magne <bjoern.onarheim@siemens-energy.com>; Opedal, Signe <signe.opedal@siemens-energy.com>; Pettersen, Tore Magnus <tore.pettersen@siemens-energy.com>; Rebnord, Paul Magnus <paul.rebnord@siemens-energy.com>; Rolfsnes, Emil Mæland <emil.rolfsnes@siemens-energy.com>; Rolfsnes, Ken Åge Ölander <ken.rolfsnes@siemens-energy.com>; Rolfsnes, Malin Sofi Ölander <malin.rolfsnes@siemens-energy.com>; Rolfsnes, Robert <robert.rolfsnes@siemens-energy.com>; Sætre, Ann Helen Nesse <ann.h.saetre@siemens-energy.com>; Sakseide, Anette <anette.sakseide@siemens-energy.com>; Siggervåg, Vidar <vidar.siggervaag@siemens-energy.com>; Skare, Viktor <viktor.skare@siemens-energy.com>; Skjellevik, Morten Åge <morten.a.skjellevik@siemens-energy.com>; Soliya, Prabhat Kiran <prabhat.k.soliya@siemens-energy.com>; Sørensen, Solfrid <solfrid.soerensen@siemens-energy.com>; Sørfonn, Monika <monika.sorfonn@siemens-energy.com>; Sortland, Arnulf <arnulf.sortland@siemens-energy.com>; Sortland, Edny Helen Siggervåg <edny.sortland@siemens-energy.com>; Speybrouck, Ruben Marc P <ruben.speybrouck@siemens-energy.com>; Stangervåg, Hans Kåre <hans.k.stangervaag@siemens-energy.com>; Stavland Kvernenes, Heidi <heidi.stavland@siemens-energy.com>; Stavland, Runar Sørvik <runar.stavland@siemens-energy.com>; Steinsland, Caroline <caroline.steinsland@siemens-energy.com>; Steinsvåg, Åse Marie <aase.m.steinsvaag@siemens-energy.com>; Stokka, Sonja <sonja.stokka@siemens-energy.com>; Stokke, Janne <janne.stokke@siemens-energy.com>; Stokke, Turid <turid.stokke@siemens-energy.com>; Stoknes, Espen <espen.stoknes@siemens-energy.com>; Størkson, Magne <magne.storkson@siemens-energy.com>; Susort, Lars Birger <lars.susort@siemens-energy.com>; Tera, Magnus <magnus.tera@siemens-energy.com>; Throndsen, Trond <trond.throndsen@siemens-energy.com>; Titlestad, Nicholai Kjellbotn <nicholai.titlestad@siemens-energy.com>; Totland, Knut Jacob <knut.j.totland@siemens-energy.com>; Tulloch, Dag Inge <dag.tulloch@siemens-energy.com>; Uddu, Trygve <trygve.uddu@siemens-energy.com>; Urangsæter, Nils Kristian <nils.k.urangsaeter@siemens-energy.com>; Urangsæter, Roy Dagfinn <roy.d.urangsaeter@siemens-energy.com>; Vabø, Richard <richard.vaboe@siemens-energy.com>; Vassdal, Berit Hagen <berit.vassdal@siemens-energy.com>; Vikane, Christian Helmersen <christian.vikane@siemens-energy.com>; Vikane, Johannes <johannes.vikane@siemens-energy.com>; Vikse, Ann Irene Lodden <ann.vikse@siemens-energy.com>; Voll, Torleif <torleif.voll@siemens-energy.com>; Vorland, Edgar <edgar.vorland@siemens-energy.com>; Wold, Tom Are <tom.a.wold@siemens-energy.com>'
# mail_addresses = mail_addresses.split(';')
# print('mail_addresses:', mail_addresses)
# corrected_mail_addresses = []
# for mail_address in mail_addresses:
#     corrected_mail_addresses.append(mail_address.strip())
# # Define the list
registered_user_list_prod_app = []
# print('number of mail addressses:', len(mail_addresses))


emails = extract_emails(mail_addresses)
print(emails)
print('number of mail addressses:', len(emails))

# Loop through each row and add it to the list
for row in sheet:
    row_text = ''
    for cell in row:
        row_text += str(cell.value) +'-'
    registered_user_list_prod_app.append(row_text)

# Print the list
# print(registered_user_list_prod_app)

registerd_gids = [
    "devtest",
    "donga00a",
    "nor27785",
    "nor28214",
    "nor28216",
    "nor28260",
    "nor28266",
    "NOR28268",
    "nor28286",
    "nor28291",
    "nor28292",
    "nor28304",
    "nor28315",
    "testlogin",
    "z002xntt",
    "Z002ZJJZ",
    "z002zuzp",
    "Z00315PJ",
    "Z00340EK",
    "Z00340EU",
    "z0034bmx",
    "Z0035FBV",
    "z0035fbx",
    "z0035fcd",
    "Z0035FCH",
    "z0035fcn",
    "Z0035FCP",
    "z0035fcr",
    "z0035fcs",
    "Z0035FCT",
    "z0035fcu",
    "z0035fcw",
    "z0035fcx",
    "z0035fdc",
    "z0035fdd",
    "z0035fdr",
    "z0035fdt",
    "Z0035FDW",
    "z0035fed",
    "z0035fee",
    "z0035fej",
    "z0035fek",
    "Z0035FER",
    "Z0035FEV",
    "z0035few",
    "z0036nhv",
    "z0036nwy",
    "z0036y2d",
    "Z0037KCR",
    "z0037s4s",
    "z00386cc",
    "z003bdfc",
    "z003d3sy",
    "z003epzw",
    "z003fhyp",
    "z003y5kj",
    "z003y66n",
    "z003y6rs",
    "z00402yv",
    "z0041ejk",
    "z0042k4m",
    "z0042wsn",
    "z0043bmu",
    "z0043cyp",
    "Z0043JCH",
    "z0043jcw",
    "Z00445TR",
    "z00449ja",
    "z00449jk",
    "z00449km",
    "z0044a3v",
    "z0044abz",
    "z0044uuf",
    "z0044v7s",
    "z0044wmy",
    "z0046bye",
    "z0046e0r",
    "z0046kks",
    "z004cx6t",
    "Z004DBFH",
    "z004jmas",
    "z004kt7e",
    "z004n34a",
    "z004p7hx",
    "z004pawt",
]

unregistered_users = []
for prod_app_user in registered_user_list_prod_app:
    user_registered = False
    for registered_gid in registerd_gids:
        if registered_gid.lower() in prod_app_user.lower():
            user_registered = True
            # print('user registered:', prod_app_user)
    if user_registered == False:
        mail_address = 'not found'
        for email in emails:
            if prod_app_user.split('-')[0].lower() in email and prod_app_user.split('-')[1].lower() in email:
                mail_address = email
    
        unregistered_users.append(prod_app_user.split('-')[0] + ' ' + prod_app_user.split('-')[1] + ' ' + prod_app_user.split('-')[4].lower() + ' ' + mail_address)
        print('new user:', prod_app_user)

print('unregistered users:', unregistered_users)
    

#write all the unregisterd users to a file
with open('unregistered_users.txt', 'w') as f:
    for item in unregistered_users:
        f.write("%s\n" % item)



