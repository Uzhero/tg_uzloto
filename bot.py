import random
import sqlite3 as sql
import time

import telebot
from PIL import Image, ImageDraw, ImageFont

import config

bot = telebot.TeleBot(config.TOKEN)
bil_narx = 1000
admin_id = 559274125
yutblt_ser = []
yut_blt = []
hisob = 10000
status_game = False
kanal_id = -1001478469577

def new_bilet(ser):
    global f
    try:
        f = open('biletlar.txt', 'a')
    except:
        print('faylni ochishda xatolik')
    f.write(str(ser) + '\n')

    bilet = [[0 for y in range(9)] for x in range(6)]
    a = []

    for i in range(6):
        a.append([])
        qator = [i for i in range(9)]
        for j in range(5):
            a[i].append(qator.pop(random.randint(0, len(qator) - 1)))

    for y in range(2):
        xalta = [[x * 10 + y for y in range(10)] for x in range(9)]
        xalta[0].remove(0)
        xalta[8].append(90)

        for i in range(3):
            for j in range(5):
                ii = 3 * y + i
                bilet[ii][a[ii][j]] = xalta[a[ii][j]].pop(random.randint(0, len(xalta[a[ii][j]]) - 1))

    for i in range(6):

        for j in range(9):
            f.write(str(bilet[i][j]) + ' ')
        f.write('\n')
    f.close()

    return bilet


def yutuqli_bilet(img, bil_belgi):
    draw = ImageDraw.Draw(img, "RGBA")
    for i in range(6):
        if i < 3:
            s = 10
        else:
            s = 20
        for j in range(9):
            if bil_belgi[i][j] == 1:
                draw.ellipse((j * 40 + 15, i * 40 + s + 5, j * 40 + 45, i * 40 + s + 35), (200, 100, 0, 180),
                             outline='orange')
    
    return img


def loto(bilet, tiraj, ser):
    image = Image.open('fon.jpg')
    #image = Image.new('RGB', (640,270), color=(200, 255, 0))
    #crop = Image.open('fon.jpg')
    #image = crop.crop((0, 0, 640, 270))
    draw = ImageDraw.Draw(image)
    for i in range(6):
        if i < 3:
            s = 10
        else:
            s = 20
        draw.rectangle((10, i * 40 + s, 370, i * 40 + s + 40), fill="white", outline="black")
    for i in range(8):
        draw.line((i * 40 + 50, 10, i * 40 + 50, 130), fill='black')
        draw.line((i * 40 + 50, 140, i * 40 + 50, 260), fill='black')

    font = ImageFont.truetype("font/19104.ttf", size=24)
    draw.text((380, 10), str(tiraj) + '\nTIRAJ', align="center", font=font, fill='white')

    font = ImageFont.truetype("font/arial.ttf", size=16)
    draw.text((380, 60), 'SER №' + '0' * (5 - len(str(ser))) + str(ser), align="center", font=font, fill='white')

    font = ImageFont.truetype("font/arial.ttf", size=18)

    for i in range(6):
        if i < 3:
            s = 10
        else:
            s = 20
        for j in range(9):
            if bilet[i][j] != 0:
                draw.text((j * 40 + 20, i * 40 + s + 10), str(bilet[i][j]), font=font, fill='black')
    del draw
    #image.show()
    # image.save("test.png", "PNG")
    return image


def yasash(n):
    con = sql.connect('regs.db', timeout=20)
    with con:
        cur = con.cursor()
        for i in range(n):
            k = f"INSERT INTO `yasalgan` VALUES ('{i}')"
            cur.execute(k)
            new_bilet(i)
        con.commit()


def game(message):
    global status_game
    
    xalta = [i + 1 for i in range(90)]
    print(xalta)
    bilet = []
    bil_belgi = []
    stol = []
    yut_id = ''
    ser_blt = ''
    con = sql.connect('regs.db', timeout=20)

    with con:
        cur = con.cursor()

        kkk = "SELECT * FROM stat"
        cur.execute(kkk)
        tiraj = len(cur.fetchall()) + 1
        kk = "SELECT * FROM s_blt "
        cur.execute(kk)
        rows = cur.fetchall()

        print(rows)


    with open('biletlar.txt', 'r') as ff:

        tmp = ff.readlines()

        for ii in range(len(rows)):
            bilet.append([])
            bil_belgi.append([])
            for j in range(6):
                bilet[ii].append(tmp[rows[ii][1] * 7 + j + 1].split())
                bil_belgi[ii].append([0 for t in range(9)])

        for y in range(len(bilet)):
            for i in range(6):
                for j in range(9):
                    bilet[y][i][j] = int(bilet[y][i][j])
        print(bilet)


    if len(bilet) > 1:
        
        sotil_blt = len(bilet)

        jackpot = int(sotil_blt*bil_narx * 0.9)
        print("Assalomu alaykum. UzLoto chiptasini sotib olib o\'yinda ishtirok etishga tayyor bo\'lib o\'tirgan kanal ishtirokchilari.\n\n Diqqat!!!"
                                               " \n O\'yinni boshlaymiz.")
        time.sleep(5)
        bot.send_message(kanal_id, "Assalomu alaykum. UzLoto chiptasini sotib olib o\'yinda ishtirok "
                                               "etishga tayyor bo\'lib o\'tirgan kanal ishtirokchilari.\n\n Diqqat!!!"
                                               " \n O\'yinni boshlaymiz.")
        time.sleep(5)
        print('O\'yinimizni bu tirajida ' + str(sotil_blt) + ' ta bilet sotildi. Va shu mablag\'ning 90% ya\'ni 💰 '  + str(jackpot) + ' aqcha o\'ynaladi.')
        bot.send_message(kanal_id, 'O\'yinimizni bu tirajida ' + str(sotil_blt) + ' ta bilet sotildi. Va shu '
                                                                                              'mablag\'ning 90% ya\'ni'
                                                                                             ' ' + str(
            jackpot) + ' aqcha o\'ynaladi.')
        time.sleep(5)
        for i in range(90):
            random.shuffle(xalta)
            raqam = xalta.pop(random.randrange(len(xalta)))
            stol.append(raqam)
            time.sleep(3)
            print(raqam)
            bot.send_message(kanal_id, raqam)
            for y in range(len(bilet)):
                for i in range(6):
                    for j in range(9):
                        if raqam == bilet[y][i][j]:
                            bil_belgi[y][i][j] = 1
            for y in range(len(bilet)):
                for i in range(6):
                    if sum(bil_belgi[y][i]) == 5:
                        yut_blt.append(y)
                        yutblt_ser.append(rows[y][1])

            if len(yut_blt) > 0:
                time.sleep(5)
                print('Diqqat yutuqli chipta!!! \n yutuqli chiptalar soni ' + str(len(yut_blt)) + ' ta')
                bot.send_message(kanal_id, 'Diqqat yutuqli chipta!!! \n yutuqli chiptalar soni ' + str(len(yut_blt)) + ' ta')

                k = "UPDATE regs SET `hisob` = hisob + " + str(sotil_blt*bil_narx-jackpot) + " WHERE idd = "+ str(admin_id)
                cur.execute(k)

                for i in range(len(yut_blt)):
                    yu = yutblt_ser[i]
                    print(yu)
                    yut_id = yut_id + ', ' + str(rows[i][2])
                    ser_blt = ser_blt + ', ' + str(rows[i][1])

                    kk = "SELECT user_id FROM s_blt where `seriya`=="+ str(yutblt_ser[i])
                    cur.execute(kk)
                    ss = cur.fetchone()

                    k = "UPDATE regs SET `hisob` = `hisob` +" + str(
                        int(jackpot/len(yut_blt))) + " WHERE `idd` == " + str(ss[0])
                    cur.execute(k)

                    print('№ ' + '0' * (5 - len(str(yu))) + str(yu))
                    time.sleep(5)
                    bot.send_message(kanal_id, '№ ' + '0' * (5 - len(str(yu))) + str(yu))
                    photo = yutuqli_bilet(loto(bilet[yut_blt[i]], tiraj, yu), bil_belgi[yut_blt[i]])

                    print('seriyali biletda yutuq chiqdi \n tabriklaymiz!!!')
                    time.sleep(5)
                    bot.send_message(kanal_id, 'seriyali biletda yutuq chiqdi \n tabriklaymiz!!! \n yutuq miqdori xar bir bilet uchun 💰 ' +str(jackpot/len(yut_blt)) + ' aqchani tashkil qiladi!')
                    bot.send_message(rows[i][2], '№ ' + '0' * (5 - len(str(yu))) + str(yu) + ' seriyali chiptangizda yutuq chiqdi!')
                    time.sleep(2)
                    bot.send_message(rows[i][2], 'Yutuq miqdori 💰 ' + str(jackpot/len(yut_blt)) + ' aqchani tashkil etdi!')
                    time.sleep(2)
                    bot.send_message(rows[i][2], 'Hisobingiz 💰 ' +str(jackpot/len(yut_blt))+ ' aqchaga to\'ldirildi!')
                    photo.save('yutuqli_bilet.png')

                    jjj = open('yutuqli_bilet.png', 'rb')

                    time.sleep(3)
                    bot.send_photo(kanal_id, jjj)
                    time.sleep(3)
                    #bot.send_photo(rows[i][2], jjj)


                print('O\'yinda ishtirok etgan raqamlar: \n' + str(stol))
                print('Qopda qolgan raqamlar:\n ' + str(xalta))

                bot.send_message(kanal_id, 'O\'yinda ishtirok etgan raqamlar: \n' + str(stol))
                bot.send_message(kanal_id, 'Qopda qolgan raqamlar:\n ' + str(xalta))
                f = open('biletlar.txt', 'w')
                f.close()


                break
        k = f"INSERT INTO `stat` VALUES (NULL, '{ser_blt}','{yut_id}','{sotil_blt}', '{jackpot}')"
        cur.execute(k)
        con.commit()
        yut_blt.clear()
        yutblt_ser.clear()
        rows.clear()
        bilet.clear()
        bil_belgi.clear()
        tmp.clear()
        k = "DROP TABLE `s_blt`"
        cur.execute(k)
        k = "DROP TABLE `yasalgan`"
        cur.execute(k)
        cur.execute("CREATE TABLE IF NOT EXISTS `s_blt` (`id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                    "`seriya` INTEGER, `user_id` INTEGER)")

        cur.execute("CREATE TABLE IF NOT EXISTS `yasalgan` (`seriya` INTEGER)")
        print(str(bilet) + '\n\n' + str(bil_belgi) + '\n\n' + str(tmp))
        con.commit()
        yasash(1000)
    elif len(bilet) == 1:
        print('Bittagina bilet sotilgan xolos. o\'yinni boshlash uchun kamida ikki kishi bilet sotib olishi kerak')
        bot.send_message(message.from_user.id,
                         'Bittagina bilet sotilgan xolos. o\'yinni boshlash uchun kamida ikki kishi bilet sotib olishi kerak')
    elif len(bilet) == 0:
        print('Hali bittayam bilet sotilgani yo\'q')
        bot.send_message(message.from_user.id, 'Hali bittayam bilet sotilgani yo\'q')

    status_game = False


@bot.message_handler(commands=['start'])
def c_start(message):
    bot.send_message(message.from_user.id, "regs")
    idd = message.from_user.id
    name = message.from_user.first_name

    con = sql.connect('regs.db', timeout=20)

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `regs` (`idd` INTEGER, `name` TEXT, `hisob` INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS `s_blt` (`id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
                    "`seriya` INTEGER, `user_id` INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS `stat` (`tiraj` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "
                    "`ser_blt` TEXT, `yut_id` TEXT, `sotil_blt` INTEGER, `jackpot` INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS `yasalgan` (`seriya` INTEGER)")
        cur.execute("SELECT idd FROM regs")
        rows = cur.fetchall()
        print(rows)

        if (idd,) in rows:
            bot.send_message(message.from_user.id, 'siz ro\'xatdan o\'tgansiz!')
        else:
            cur.execute(f"INSERT INTO `regs` VALUES ('{idd}','{name}','{hisob}')")
            bot.send_message(idd, 'TABRIKLAYMIZ!!!\n Siz ro\'xatdan o\'tdingiz!\n Hisobingizga 💰' + str(
                hisob) + ' aqcha o\'tkazildi. Hisobingizni tekshirish uchun /hisob buyrug\'ini ishlating.')


@bot.message_handler(commands=['bilet'])
def bilet_olish(message):
    global status_game
    
    con = sql.connect('regs.db', timeout=20)
    us_id = message.from_user.id
    with con:
        bilet = []
        cur = con.cursor()

        k = "UPDATE regs SET 'hisob'= hisob -1000 where idd =" + str(us_id)
        cur.execute("SELECT `hisob` FROM regs WHERE `idd` ==" + str(us_id))
        rows = cur.fetchone()
        if status_game == 0:
            if rows[0] >= bil_narx:
                cur.execute(k)
                kkk = "SELECT * FROM yasalgan"
                cur.execute(kkk)
                sr = cur.fetchall()
                s = sr[random.randint(0, len(sr)-1)][0]
                print(len(sr))
                print(s)
                kkk = "DELETE FROM `yasalgan` WHERE `seriya` == " + str(s)
                cur.execute(kkk)
                kkk = "SELECT * FROM stat"
                cur.execute(kkk)
                tiraj = len(cur.fetchall()) + 1
                
                kkk = f"INSERT INTO `s_blt` VALUES (NULL,'{s}', '{us_id}')"
                cur.execute(kkk)
                with open('biletlar.txt', 'r') as ff:
                    tmp = ff.readlines()

                    ser = tmp[s * 7]
                    for j in range(6):
                        bilet.append(tmp[s*7+j+1].split())
                    for i in range(6):
                        for j in range(9):
                            bilet[i][j] = int(bilet[i][j])
                    print(bilet)
                img = loto(bilet, tiraj, s)
                img.save("bilet.png")

                file = open("bilet.png", 'rb')
                bot.send_photo(message.from_user.id, file)
            else:
                print('Hisobingiz pul yetarli emas. Oldin hisobingizni to\'ldiring.\n Hisobni to\'ldirish uchun @uz_hero ga murojaat qiling.')
                bot.send_message(message.from_user.id,
                                 'Hisobingiz pul yetarli emas. Oldin hisobingizni to\'ldiring.\n Hisobni to\'ldirish uchun '
                                 '@uz_hero ga murojaat qiling.')
        else:
            print('Biletni o\'yin tugagandan keyin xarid qilishingiz mumkin bo\'ladi')
            bot.send_message(message.from_user.id, 'Biletni o\'yin tugagandan keyin xarid qilishingiz mumkin bo\'ladi')
        con.commit()


@bot.message_handler(commands=['hisob'])
def kissa(message):
    con = sql.connect('regs.db', timeout=15)

    with con:
        cur = con.cursor()
        k = "SELECT hisob FROM regs where idd=" + str(message.from_user.id)
        cur.execute(k)
        rows = cur.fetchone()
        bot.send_message(message.from_user.id, '💰 ' + str(rows[0]))


@bot.message_handler(commands=['begin'])
def c_begin(message):
    global status_game
    if message.from_user.id == 559274125 and not status_game:
        status_game = True
        game(message)
    elif message.from_user.id == 559274125 and status_game:
        bot.send_message(message.from_user.id, 'O\'yin boshlanib bo\'ldi')

@bot.message_handler(commands=['id'])
def id(message):
    bot.send_message(message.from_user.id, str(message.from_user.id))

@bot.message_handler(content_types=['text'])
def send_coin(message):
    msg = message.text.split()
    con=sql.connect('regs.db', timeout=10)


    if len(msg) == 3:
        if msg[0]== 'send':
            if int(msg[1]) != None and int(msg[2]) > 0:
                with con:
                    cur = con.cursor()

                    k = "SELECT idd FROM regs"
                    cur.execute(k)
                    rows = cur.fetchall()
                    print(rows)
                    print(msg)
                    if (int(msg[1]),) in rows:
                        k = "SELECT hisob FROM regs WHERE idd=="+str(msg[1])
                        cur.execute(k)
                        hsb=cur.fetchone()
                        if hsb[0] > int(msg[2]):
                            k = "UPDATE regs set `hisob` = hisob +"+str(msg[2]) +" where `idd` == "+ str(msg[1])
                            cur.execute(k)
                            k = "UPDATE regs set `hisob` = hisob -" + str(msg[2]) + " where `idd` == " + str(message.from_user.id)
                            cur.execute(k)
                            bot.send_message(message.from_user.id, 'Pul o\'tkazish muvoffaqiyatli yakunlandi.')
                            bot.send_message(int(msg[1]), 'Sizning hisobingiz ' + msg[2] + ' aqchaga to\'ldirildi.')
                        else:
                            bot.send_message(message.from_user.id, 'Hisobiningizdagi pul '+ msg[2]+ ' aqchadan kam!')
                    else:
                        bot.send_message(message.from_user.id, 'Bunday id raqamli foydalanuvchi ro\'yxatdan o\'tmagan!')

            else:
                bot.send_message(message.from_user.id, 'Komandani xato kiritdingiz. Qaytadan to\'g\'rilab yozing')

        #bot.send_message(message.from_user.id, 'togri')

bot.polling()
