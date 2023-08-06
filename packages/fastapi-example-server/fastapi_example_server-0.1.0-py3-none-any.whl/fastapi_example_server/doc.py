try:
    import sphinx.cmd.build as sphinx_build
    import sphinx.ext.apidoc as sphinx_apidoc
except ImportError as exc:
    print("dev dependencies must be installed to generate documentation")


def main():
    sphinx_apidoc.main(["-o", "docs/source/gen", "project"])
    sphinx_build.main(["docs/source", "docs/build"])


if __name__ == "__main__":
    main()
