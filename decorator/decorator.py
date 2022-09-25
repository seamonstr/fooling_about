def mydecorator(method):
    print(f"Decorating method {method}")

    def decorate():
        print(f"Calling method {method}")
        method()

    return method


@mydecorator
def mymethod():
    print("Running mymethod!")


def main():
    print("Let's go!")
    mymethod()


if __name__ == "__main__":
    main()
