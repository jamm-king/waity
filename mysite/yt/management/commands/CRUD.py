from django.core.management.base import BaseCommand
from yt.models import *
from yt.setup.views import *
from time import sleep
import os

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class Command(BaseCommand):
    help = '커맨드에 대한 도움말을 적어줌'

    def CREATE_Channel(self):
        clearConsole()
        print("--------------------------------------------------")
        print("                  CREATE Channel")
        print("--------------------------------------------------")
        setup_Channel()
        make_keywordTag()
        setup_Video()
        sleep(2)
        return

    def CREATE_KingTag(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                 CREATE KingTag")
            print("--------------------------------------------------")
            tag_name = input('tag_name: ')
            address_name = input('address_name: ')
            id = input('id: ')
            parentTag_name = input('parentTag_name: ')
            try:
                parentTag = KingTag.objects.filter(tag_name=parentTag_name).get()
                KingTag.objects.create(tag_name=tag_name, address_name=address_name, parentTag=parentTag, id=id)
                print(tag_name, 'created')
                sleep(2)
                return
            except:
                print('Wrong parent tag name')
        return

    def CREATE_CSV(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                   CREATE CSV")
            print("         1. To train  2. To verify  3. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                try:
                    CSV_train()
                    print('CSVs created')
                except:
                    print('Creating CSVs failed')
            if c == '2':
                try:
                    CSV_verify()
                    print('CSVs created')
                except:
                    print('Creating CSVs failed')
            if c == '3':
                return

    def CREATE(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                     CREATE")
            print("        1. Channel  2. KingTag  3. CSV  4. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                self.CREATE_Channel()
            if c == '2':
                self.CREATE_KingTag()
            if c == '3':
                self.CREATE_CSV()
            if c == '4':
                return
        return

    def READ_Videos(self, channel):
        clearConsole()
        videos = channel.video.all()
        while 1:
            print("--------------------------------------------------")
            print("     Videos of", channel.chan_title)
            print("--------------------------------------------------")
            for i, video in enumerate(videos):
                tags = video.tag.all()
                print(i+1, video.title, end=' || ')
                for tag in tags:
                    print(tag, end=' ')
                print()
            print("--------------------------------------------------")
            print("             Press any key to go Back")
            print("--------------------------------------------------")
            c = input()
            return

    def READ_Channel_Title(self, title):
        try:
            channel = Channel.objects.filter(chan_title=title).get()
        except:
            print("No channel found. Enter the right title.")
            sleep(2)
            return False
        tags = channel.tag.all()
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("Title:", channel.chan_title)
            print("ID:", channel.chan_id)
            print("Tag: ", end='')
            for tag in tags:
                print(tag, end=' ')
            print()
            print("--------------------------------------------------")
            print("            1. View Videos  2. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                self.READ_Videos(channel)
            if c == '2':
                return True
        return True

    def READ_Channel_Tag(self):
        tag_name = input('Tag: ')
        tag = Tag.objects.filter(tag_name=tag_name).get()
        channels = tag.tagged.all()
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            for i, channel in enumerate(channels):
                print(i+1, channel.chan_title)
            print('0 Back')
            print("--------------------------------------------------")
            c = int(input()) - 1
            if c == -1:
                return
            try:
                channel = channels[c]
                self.READ_Channel_Title(channel.chan_title)
            except:
                print("Wrong number. Try again.")
        return

    def READ_Channel(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                   READ Channel")
            print("            1. Title  2. Tag  3. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                flag = False
                while not flag:
                    title = input('Channel Title: ')
                    flag = self.READ_Channel_Title(title)
            if c == '2':
                self.READ_Channel_Tag()
            if c == '3':
                return
        return

    def READ_ToFix(self):
        TF = ToFix.objects.all()
        if TF.count() != 0:
            clearConsole()
            print("--------------------------------------------------")
            print("                      ToFix")
            print("--------------------------------------------------")
            for i, tf in enumerate(TF):
                print(i+1, Channel.objects.filter(chan_id=tf.chan_id).get().chan_title, '\t' ,tf.errorType)
            print("--------------------------------------------------")
            print("             Press any key to go Back")
            print("--------------------------------------------------")
            c = input()
            return
        else:
            print("There's nothing to fix.")
            sleep(2)
            return

    def READ_Tag(self, tag_name):
        try:
            tag = KingTag.objects.filter(tag_name=tag_name).get()
            parentTag = tag.parentTag
        except:
            print("No tag found. Enter the right title.")
            sleep(2)
            return False

        clearConsole()
        print("--------------------------------------------------")
        print("tag_name:", tag.tag_name)
        print("address_name:", tag.address_name)
        print("parent tag:", parentTag)
        print("--------------------------------------------------")
        print("             Press any key to go Back")
        print("--------------------------------------------------")
        c = input()
        return True

    def READ(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                      READ")
            print("    1. Channel  2. ToFix  3. KingTag  4. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                self.READ_Channel()
            if c == '2':
                self.READ_ToFix()
            if c == '3':
                flag = False
                while not flag:
                    tag_name= input('tag: ')
                    flag = self.READ_Tag(tag_name)
            if c == '4':
                return
        return

    def UPDATE(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                      UPDATE")
            print("              1. Channel  2. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                UPDATE()
            if c == '2':
                return
        return

    def DELETE(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                     DELETE")
            print("        1. Channel  2. Tag  3.ToFix  4. Back")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                while 1:
                    title = input('title: ')
                    try:
                        channel = channel.objects.filter(chan_title=title).get()
                        channel.delete()
                        break
                    except:
                        print('No channel found. Try again.')
                        sleep(2)
            if c == '2':
                 while 1:
                    tag_name = input('tag: ')
                    try:
                        tag = Tag.objects.filter(tag_name=tag_name).get()
                        tag.delete()
                        break
                    except:
                        print('No tag found. Try again.')
                        sleep(2)
            if c == '3':
                clearConsole()
                handle_ToFix()
                sleep(2)
            if c == '4':
                return
        return

    def Interface(self):
        while 1:
            clearConsole()
            print("--------------------------------------------------")
            print("                   CRUD for Waity")
            print("1. CREATE  2. READ  3. UPDATE  4. DELETE  5. EXIT")
            print("--------------------------------------------------")
            c = input()
            if c == '1':
                self.CREATE()
            if c == '2':
                self.READ()
            if c == '3':
                self.UPDATE()
            if c == '4':
                self.DELETE()
            if c == '5':
                break
        return

    def handle(self, *args, **kwargs):
        self.Interface()
        return