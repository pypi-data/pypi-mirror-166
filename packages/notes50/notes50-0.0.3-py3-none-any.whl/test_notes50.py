from project import parse_args, note, pset

tNotes = {
    "a": 0,
    "g": 0,
    "p": 0,
    "w": 0,
    "x": 0,
}

tPsets = {
    "a": "0/degrees",
    "g": "0/pong",
    "p": "0/indoor",
    "w": "0/search",
    "x": "0/scratch",
}

tProjects = {
    "g": "project",
    "p": "project",
    "w": "project",
    "x": "project",
}


def test_notes():
    for key, value in tNotes.items():
        args = parse_args([f"-{key}", value])
        for i in vars(args):
            if f"{getattr(args, i)}".isnumeric():
                with open("tests/temp.md", "w+")as t:
                    t.write(note(args, i))
                with open(f"./tests/{key}/{value}.md") as f:
                    with open("tests/temp.md") as t:
                        print(key, value)
                        assert t.read() == f.read()


def test_psets():
    for key, value in tPsets.items():
        args = parse_args([f"-{key}", value])
        for i in vars(args):
            if f"{getattr(args, i)}".isnumeric():
                with open("tests/temp.md", "w+")as t:
                    t.write(pset(args, i))
                with open(f"./tests/{key}/{value}.md") as f:
                    with open("temp.md") as t:
                        assert t.read() == f.read()


def test_projects():
    for key, value in tProjects.items():
        args = parse_args([f"-{key}", value])
        for i in vars(args):
            if f"{getattr(args, i)}".isnumeric():
                with open("tests/temp.md", "w+")as t:
                    t.write(pset(args, i))
                with open(f"./tests/{key}/{value}.md") as f:
                    with open("temp.md") as t:
                        assert t.read() == f.read()


def main():
    test_notes()
    test_projects()
    test_psets()


main()
