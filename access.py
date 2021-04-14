"""
William Morley
CS 465
Programming Assignment 2 - Access Control
"""

import cmd
import sys

# set variable for instruction text file
instruct_file = sys.argv[1]
# create an audit log text file
audit_log = open("audit.txt", "w+")
# added friends list
friend_list_struc = []
# text file for lists
list_text = open("lists.txt", "w+")
# user profile has not been created for profile owner yet
created = False
# user profile has not been viewed by profile owner yet
viewed_root = False
# a user is viewing the profile
being_viewed = False
# who is viewing profile
being_viewed_by = ""
# dictionary of lists that have been added
list_dict = {}
# dictionary for pictures
pic_dict = {}
# file for picture.txt
pictures_log = open("pictures.txt", "w+")
# dictionary for permissions
perm_dict = {}


class MyFacebook(cmd.Cmd):
    # input is from text file not entered by user
    use_rawinput = False;

    # no prompt for user
    prompt = ""

    # friendadd command
    def do_friendadd(self, friend_name):
        global created
        # if root is the friend name, root is added to the audit log and displayed to user.
        # profile is created for root user and created variable is set
        if friend_name == "root":
            friend_list = open("friends.txt", "w+")
            friend_list_struc.append(friend_name)
            friend_list.write(friend_name + "\n")
            print("Friend " + friend_name + " added")
            audit_log.write("Friend " + friend_name + " added \n")
            created = True

        # checks if root has created a profile, if not program exits.
        # checks if friend has already been added to the list data structure which contains added friends
        # if name has not been added already, program adds friend. displays to user and writes to log
        else:
            if not created:
                print("Error: You have not created a profile yet.")
                print("Goodbye. ")
                exit()
            if friend_name in friend_list_struc:
                print("This friend, " + friend_name + ", has already been added. ")
                audit_log.write("This friend, " + friend_name + ", has already been added. \n")
            else:
                friend_list = open("friends.txt", "a+")
                friend_list_struc.append(friend_name)
                friend_list.write(friend_name + "\n")
                audit_log.write("Friend " + friend_name + " added \n")
                print("Friend " + friend_name + " added")

    # viewby command
    def do_viewby(self, friend_name):
        global viewed_root
        global being_viewed
        global being_viewed_by
        # if root user views profile, it is displayed and written to log
        # profile is viewed by root user and viewed_root is set
        if friend_name == "root":
            print("User " + friend_name + " views the profile ")
            audit_log.write("User " + friend_name + " views the profile \n")
            viewed_root = True
            being_viewed = True
            being_viewed_by = friend_name

        # checks if the root user has viewed profile, if not program exits and is displayed/ written to log
        # checks if friend trying to view profile is in the added friends list
        # checks if a friend is already viewing profile, if so an error is given.
        # if a friend is not already viewing profile, friend trying to view profile is allowed and written to log
        # if someone trying to view profile is not a friend an error is given
        else:
            if viewed_root == False:
                print("Error: profile has not been viewed by owner yet")
                print("Goodbye ")
                exit()
            else:
                if friend_name in friend_list_struc:
                    if being_viewed == False:
                        print("User " + friend_name + " views the profile ")
                        audit_log.write("User " + friend_name + " views the profile \n")
                        being_viewed = True
                        being_viewed_by = friend_name
                    else:
                        print("View Failed: Concurrent friends not supported")
                        audit_log.write("View Failed: Concurrent friends not supported \n")
                else:
                    print("Error: " + friend_name + " has not been added as a friend and cannot view profile")
                    audit_log.write("Error: " + friend_name + " has not been added as a friend and cannot view profile \n")

    # logout command
    def do_logout(self, arg):
        # global variables to keep track if the profile is being viewed and by who
        global being_viewed
        global being_viewed_by

        # if the profile is being viewed by someone then that person is logged out
        # if no one is viewing the profile that is displayed to the console
        if being_viewed == True:
            print("Friend " + being_viewed_by + " logged out")
            audit_log.write("Friend " + being_viewed_by + " logged out \n")
            being_viewed = False
            being_viewed_by = ""
        else:
            print("No one is viewing profile. ")

    # listadd command
    def do_listadd(self, list_name):
        # to add the list the root user must be the one viewing the profile
        # if the list is not in the list dictionary then the list is added and logged
        # if the list has already been created this is displayed to the console
        # if the a user which is not root tries to add a list, the list is not added and message is displayed
        if being_viewed_by == "root":
            if list_name not in list_dict:
                list_dict[list_name] = []
                print("List " + list_name + " created")
                audit_log.write("List " + list_name + " created \n")
            else:
                print("List has already been created")
                audit_log.write("List has already been created")
        else:
            print("User does not have authorization to create list ")
            audit_log.write("User does not have authorization to create list ")

    # friendlist command
    def do_friendlist(self, arg):
        # parse the command and split to the appropriate variables
        arg_list = arg.split()
        friend_name = arg_list[0]
        list_name = arg_list[1]

        # only the root user has the ability to add friends to lists
        # if the friend has not been previously added to the friend list then the message is displayed
        # checks if the list has already been created, if not adds the list to the dictionary
        # checks if the friend has already been added to the list, if so a message is displayed
        # if the friend is not in the list and the list exists then the friend is added to the list
        if being_viewed_by == "root":
            if friend_name not in friend_list_struc:
                print("This friend, " + friend_name + ", has not been added ")
                audit_log.write("This friend, " + friend_name + ", has not been added \n")
            else:
                if list_name not in list_dict.keys():
                    print("The list, " + list_name + ", has not been added yet ")
                    audit_log.write("The list, " + list_name + ", has not been added yet \n")
                else:
                    if friend_name in list_dict[list_name]:
                        print("This friend is already in the list ")
                    else:
                        list_dict[list_name].append(friend_name)
                        list_text.write(list_name + ": " + friend_name + "\n")
                        print("Friend, " + friend_name + ", has been added to " + list_name)
                        audit_log.write("Friend, " + friend_name + ", has been added to " + list_name + "\n")
        else:
            print("User does not have authorization to add to list")
            audit_log.write("User does not have authorization to add to list \n")

    # postpicture command
    def do_postpicture(self, picture_name):
        # if no one is currently viewing the profile an error is displayed and picture is not posted.
        # if someone is viewing the profile, the program checks if a picture with the same name has already been created
        # if the picture name has not been used, the program adds the pic to the dictionary with owner, nil list and default permissions
        # the picture name, owner, list and permissions are written to pictures.txt
        # the program then creates text files associated with each picture
        if being_viewed == False:
            print("No one is viewing the profile. Picture can not be posted. ")
            audit_log.write("No one is viewing the profile. Picture can not be posted. ")
        else:
            if picture_name in pic_dict.keys():
                print("A picture with this name has already been created ")
                audit_log.write("A picture with this name has already been created ")
            else:
                pic_dict[picture_name] = {}
                pic_dict[picture_name]["owner"] = being_viewed_by
                pic_dict[picture_name]["list"] = "nil"
                pic_dict[picture_name]["permissions"] = "rw -- --"
                perm_dict[picture_name] = {}
                perm_dict[picture_name]["owner"] = "rw"
                perm_dict[picture_name]["list"] = "--"
                perm_dict[picture_name]["others"] = "--"
                print("Picture " + picture_name + " with owner " + pic_dict[picture_name]["owner"] + " and default permissions"
                                                                                                    " has been created")
                audit_log.write("Picture " + picture_name + " with owner " + pic_dict[picture_name]["owner"] + " and default permissions"
                                                                                                    " has been created \n")
                pic_file = open(picture_name, "w+")
                pictures_log.write(picture_name + ": " + pic_dict[picture_name]["owner"] + " " + pic_dict[picture_name]["list"]
                                   + " " + pic_dict[picture_name]["permissions"] + " \n")

    # chlist command
    def do_chlst(self, args):
        # arguments are split into their respective variables
        # if the profile is not being viewed an error is displayed and logged
        # if the picture has not been added, and error is displayed and logged
        # checks if the user viewing is the picture owner or root user
        # if the list has not been created then an error is displayed
        # if the list has been created, the picture list is changed appropriately
        # if the person viewing the profile is not authorized to change the list associated an error is displayed and logged
        arg_list = args.split()
        picture_name = arg_list[0]
        list_name = arg_list[1]
        if being_viewed == False:
            print("Cannot change list for picture when no one is viewing profile")
            audit_log.write("Cannot change list for picture when no one is viewing profile")
        else:
            if picture_name not in pic_dict.keys():
                print("This picture does not exist ")
                audit_log.write("This picture does not exist \n")
            else:
                if being_viewed_by == pic_dict[picture_name]["owner"] or "root":
                    if list_name not in list_dict.keys():
                        print("This list does not exist ")
                        audit_log.write("This list does not exist \n")
                    else:
                        if list_name == "nil":
                            pic_dict[picture_name]["list"] = "nil"
                            print("List for " + picture_name + " has been changed to " + list_name + " by " + being_viewed_by)
                            audit_log.write("List for " + picture_name + " has been changed to " + list_name + " by " + being_viewed_by + "\n")
                        else:
                            pic_dict[picture_name]["list"] = list_name
                            print(
                                "List for " + picture_name + " has been changed to " + list_name + " by " + being_viewed_by)
                            audit_log.write(
                                "List for " + picture_name + " has been changed to " + list_name + " by " + being_viewed_by + "\n")
                else:
                    print("You do not have authorization to change list for this picture ")
                    audit_log.write("You do not have authorization to change list for this picture \n")

    #chmod command
    def do_chmod(self, args):
        # split method args into respective variables
        # check if the picture has been added
        # if picture has been added, check if the profile is being viewed by the picture owner or root user
        # if correct person is viewing, set permissions for the picture and write those to console and log
        # if not pic owner or root tries to change permissions or the picture does not exist a message is displayed and logged
        args_list = args.split()
        picture_name = args_list[0]
        owner_perm = args_list[1]
        list_perm = args_list[2]
        others_perm = args_list[3]
        if picture_name in pic_dict.keys():
            if being_viewed_by == pic_dict[picture_name]["owner"] or "root":
                perm_dict[picture_name]["owner"] = owner_perm
                perm_dict[picture_name]["list"] = list_perm
                perm_dict[picture_name]["others"] = others_perm
                print("Permissions for " + picture_name + " set to " + " " + owner_perm + " " + list_perm + " " + others_perm
                      + " by " + being_viewed_by)
                audit_log.write("Permissions for " + picture_name + " set to " + " " + owner_perm + " " + list_perm + " " + others_perm
                      + " by " + being_viewed_by + "\n")
            else:
                print("The owner of this picture has to change modes ")
                audit_log.write("The owner of this picture has to change modes \n")
        else:
            print("This picture has not been added ")
            audit_log.write("This picture has not been added \n")

    #chowm command
    def do_chown(self, args):
        # splits args into their respective variables
        # checks to see if root user is viewing the profile
        # checks if picture has been created and if friend has been added
        # if picture has been created and friend has been added then the owner of the picture is changed
        # if picture has not been created or friend has not been added a message is displayed and logged
        # if profile owner is not the one to call command then a message is displayed and logged
        arg_list = args.split()
        picture_name = arg_list[0]
        friend_name = arg_list[1]
        if being_viewed_by == "root":
            if picture_name in pic_dict.keys():
                if friend_name in friend_list_struc:
                    pic_dict[picture_name]["owner"] = friend_name
                    print("Owner of " + picture_name + " has been changed to " + friend_name)
                    audit_log.write("Owner of " + picture_name + " has been changed to " + friend_name + "\n")
                else:
                    print("This friend has not been added. ")
                    audit_log.write("This friend has not been added \n")
            else:
                print("This picture does not exist. ")
                audit_log.write("This picture does not exist \n")
        else:
            print("This command can only be executed by the profile owner")
            audit_log.write("This command can only be executed by the profile owner \n")

    #readcomments command
    def do_readcomments(self, picture_name):
        # checks if the picture has been added
        if picture_name in pic_dict.keys():
            # checks if the person viewing is a friend
            if being_viewed_by in friend_list_struc:
                # checks if the person viewing profile owns the picture
                if being_viewed_by == pic_dict[picture_name]["owner"]:
                    # checks if the owner has reading permissions, if so the command is executed and comments displayed and logged
                    if perm_dict[picture_name]["owner"][0] == "r":
                        print("Friend " + being_viewed_by + " reads from " + picture_name + " as: ")
                        open_pic = open(picture_name, "r+")
                        audit_log.write("Friend " + being_viewed_by + " reads from " + picture_name + " as: \n")
                        for lines in open_pic:
                            print(lines)
                            audit_log.write(lines + " \n")
                    # if the owner does not have reading permissions the command is denied and logged
                    else:
                        print("Friend " + being_viewed_by + " denied read access to " + picture_name)
                        audit_log.write("Friend " + being_viewed_by + " denied read access to " + picture_name + "\n")
                # checks if the list associated with picture is added and if the friend viewing is part of that list
                elif pic_dict[picture_name]["list"] in list_dict.keys() and being_viewed_by in list_dict[pic_dict[picture_name]["list"]]:
                    # if friends in list have reading permissions command is executed, comments displayed and logged
                    if perm_dict[picture_name]["list"][0] == "r":
                        print("Friend " + being_viewed_by + " reads from " + picture_name + " as: ")
                        open_pic = open(picture_name, "r+")
                        audit_log.write("Friend " + being_viewed_by + " reads from " + picture_name + " as: \n")
                        for lines in open_pic:
                            print(lines)
                            audit_log.write(lines + "\n")
                    # if friend in list does not have permission the command is denied and logged
                    else:
                        print("Friend " + being_viewed_by + " denied read access to " + picture_name)
                        audit_log.write("Friend " + being_viewed_by + " denied read access to " + picture_name + "\n")
                # if others have reading permissions the command is executed and comments are displayed and logged
                elif perm_dict[picture_name]["others"][0] == "r":
                    print("Friend " + being_viewed_by + " reads from " + picture_name + " as: ")
                    open_pic = open(picture_name, "r+")
                    audit_log.write("Friend " + being_viewed_by + " reads from " + picture_name + " as: \n")
                    for lines in open_pic:
                        print(lines)
                        audit_log.write(lines + "\n")
                # if others do not have permissions to read then access is denied
                else:
                    print("Friend " + being_viewed_by + " denied read access to " + picture_name)
                    audit_log.write("Friend " + being_viewed_by + " denied read access to " + picture_name + "\n")
            # if you are not an added friend permission is denied
            else:
                print("The person trying to view is not an added friend ")
                audit_log.write("The person trying to view is not an added friend \n")
        # if picture has not been created the message is displayed and logged
        else:
            print("This picture has not been created ")
            audit_log.write("This picture has not been created ")

    #writecomments command
    def do_writecomments(self, args):
        # split args into picture name and the text to be commented
        args_list = args.split(" ", 1)
        picture_name = args_list[0]
        some_text = args_list[1]
        # checks if the picture has been created
        if picture_name in pic_dict.keys():
            # checks if the person viewing is a friend
            if being_viewed_by in friend_list_struc:
                # checks if the person viewing is the owner of the picture
                if being_viewed_by == pic_dict[picture_name]["owner"]:
                    # checks if the owner has writing permission, if so the comments are written to file and logged
                    if perm_dict[picture_name]["owner"][1] == "w":
                        open_pic = open(picture_name, "a+")
                        open_pic.write(some_text +"\n")
                        print("Friend " + being_viewed_by + " wrote to " + picture_name + ": " + some_text)
                        audit_log.write("Friend " + being_viewed_by + " wrote to " + picture_name + ": " + some_text + "\n")
                    # if friend does not have writing permissions then command is denied and logged
                    else:
                        print("Friend " + being_viewed_by + "denied write access to " + picture_name)
                        audit_log.write("Friend " + being_viewed_by + "denied write access to " + picture_name + "\n")
                # checks if the picture is associated with list and friend is added to the list
                elif pic_dict[picture_name]["list"] in list_dict.keys() and being_viewed_by in list_dict[pic_dict[picture_name]["list"]]:
                    # if so, and the picture gives writing permissions to friend, comments are added and logged
                    if perm_dict[picture_name]["list"][1] == "w":
                        open_pic = open(picture_name, "a+")
                        open_pic.write(some_text + "\n")
                        print("Friend " + being_viewed_by + " wrote to : " + picture_name + ": " + some_text)
                        audit_log.write("Friend " + being_viewed_by + " wrote to : " + picture_name + ": " + some_text + "\n")
                    # if no, the friend is denied writing permissions to the picture
                    else:
                        print("Friend " + being_viewed_by + "denied write access to " + picture_name)
                        audit_log.write("Friend " + being_viewed_by + "denied write access to " + picture_name + "\n")
                # if others are given writing permissions then comments are written and logged
                elif perm_dict[picture_name]["others"][1] == "w":
                    open_pic = open(picture_name, "a+")
                    open_pic.write(some_text + "\n")
                    print("Friend " + being_viewed_by + " wrote to : " + picture_name + ": " + some_text)
                    audit_log.write("Friend " + being_viewed_by + " wrote to : " + picture_name + ": " + some_text + "\n")
                # if writing permissions are denied to others, message is displayed and logged
                else:
                    print("Friend " + being_viewed_by + " denied write access to " + picture_name)
                    audit_log.write("Friend " + being_viewed_by + " denied write access to " + picture_name + "\n")
            # if you are not an added friend permission is denied
            else:
                print("The person trying to view is not an added friend ")
                audit_log.write("The person trying to view is not an added friend ")
        # if picture has not been created the message is displayed and logged
        else:
            print("This picture has not been created ")
            audit_log.write("This picture has not been created ")

    #end of file command
    def do_end(self, arg):
        sys.exit()


if __name__ == '__main__':
    instruction_file = open(sys.argv[1], 'rt')
    try:
        MyFacebook(stdin=instruction_file).cmdloop()
    finally:
        instruction_file.close()

