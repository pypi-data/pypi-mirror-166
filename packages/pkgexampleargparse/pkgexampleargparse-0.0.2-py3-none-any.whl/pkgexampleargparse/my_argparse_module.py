import argparse

def my_string_list():
    my_string_list_parser = argparse.ArgumentParser(description="My 'str list' Argparse Script")
    my_string_list_parser.add_argument('input_strings',metavar='S',type=str, nargs='+', help="A list of strings you want to concatinate."  )

    my_args = my_string_list_parser.parse_args()

    if my_args.input_strings:
        return ''.join(my_args.input_strings)

def my_int_list():
    my_int_list_parser = argparse.ArgumentParser(description="My 'int list' Argparse Script")
    my_int_list_parser.add_argument('input_numbers',metavar='N',type=int, nargs=2, help="Two numbers you want to add"  )
    
    my_args = my_int_list_parser.parse_args()

    if my_args.input_numbers:
        my_numbers=my_args.input_numbers 
        my_sum=my_numbers[0]+my_numbers[1] 
        print(my_sum)


def my_store():
    my_store_parser = argparse.ArgumentParser(description="My 'Store' Argparse Script")
    my_store_parser.add_argument('-l','--my-language', choices=['French','English','German'],help="Choose your language. ",default='English')

    my_args = my_store_parser.parse_args()

    if type(my_args.my_language) is str:
        if (my_args.my_language).lower() == "french":
            print("Bonjour le monde!")
        elif (my_args.my_language).lower() == "english":
            print("Hello World!")
        elif (my_args.my_language).lower() == "german":
            print("Hallo Welt!")
        else:
            print("Only French, English and German languages are supported.") 

   

def my_store_const():
    my_store_const_parser = argparse.ArgumentParser(description="My 'Store Const' Argparse Script")
    my_store_const_parser.add_argument('-c','--cat', action='store_const', const='Meow', help='Set cat animal sound.')
    my_store_const_parser.add_argument('-d','--dog', action='store_const', const='Woof Woof', help='Set dog animal sound.')
    
    my_args = my_store_const_parser.parse_args()
    if my_args.cat is not None:
        print(f"Did you just hear something go \"{my_args.cat}\" !!!!!")
    if my_args.dog is not None:
        print(f"Did you just hear something go \"{my_args.dog}\" !!!!!")
    

def my_bool():
    my_bool_parser = argparse.ArgumentParser(description="My Bool Argparse Script")
    my_bool_parser.add_argument('--is-hot', action='store_true')
    
    my_args = my_bool_parser.parse_args()

    print(my_args.is_hot)


#groups

def my_groups():
    main_group_parser = argparse.ArgumentParser(description="My 'Group Argument' Argparse Script",prog='my_program_name',add_help=True)

    group1 = main_group_parser.add_argument_group('group1', 'My group 1 description!')
    group1.add_argument('-c','--cat-said', help="What did the cats say?")



    group2 = main_group_parser.add_argument_group('group2', 'My group 2 description!')
    group2.add_argument('-f','--fox-said', help='What did the fox say?')


    my_args=main_group_parser.parse_args()

    if my_args.cat_said is not None:
        print(f"The cat said \"{my_args.cat_said}\" !!")


    if my_args.fox_said is not None:
        print(f"The fox said \"{my_args.fox_said}\" !!")


def my_subparser():

    def subcommand(func):
        def wrapper(*args,**kwargs):
            if my_args.simon_says == True:
                return func(*args,**kwargs)
            else:
                print("Ah ah ah... you didn't say Simon Says.")
        return wrapper
        

    @subcommand
    def animalsaid():
        if my_args.cat_said is not None:
            print(f"The cat said \"{my_args.cat_said}\" ")

    @subcommand
    def add2numbers():
         if my_args.input_numbers is not None:
                my_numbers=my_args.input_numbers 
                my_sum=my_numbers[0]+my_numbers[1] 
                print(my_sum)

    my_toplevel_parser = argparse.ArgumentParser()
    my_toplevel_parser.add_argument('--simon-says', action='store_true', help='If this switch isn\'t given, commands won\'t work.')

    subparsers = my_toplevel_parser.add_subparsers(help='Available subcommands')

    parser_a = subparsers.add_parser('animalsaid',help='Tell us what the animal said, supply a string.')
    parser_a.add_argument('-c','--cat-said', help='What did the cat say?')
    parser_a.set_defaults(func=animalsaid)

    parser_b = subparsers.add_parser('add2numbers',help='Use this command to add two integers.')
    parser_b.add_argument('input_numbers',metavar='N',type=int, nargs=2, help="Two numbers you want to multiply"  )
    parser_b.set_defaults(func=add2numbers)

    my_args=my_toplevel_parser.parse_args()

    my_args.func()




    