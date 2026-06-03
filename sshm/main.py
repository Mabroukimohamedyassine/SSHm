try:
    from .session import Session
except ImportError:
    from sshm.session import Session


def main():
    Session().run()


if __name__ == "__main__":
    main()
