# Documentation: https://docs.brew.sh/Formula-Cookbook
#                https://rubydoc.brew.sh/Formula
class NeoSays < Formula
  include Language::Python::Virtualenv

  desc "A snarky CLI fortune teller for developers"
  homepage "https://github.com/mongsill6/neo-says"
  url "https://github.com/mongsill6/neo-says/archive/refs/tags/v7.0.0.tar.gz"
  # TODO: Update SHA256 after release — run:
  #   curl -sL https://github.com/mongsill6/neo-says/archive/refs/tags/v7.0.0.tar.gz | shasum -a 256
  sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.12"

  resource "rich" do
    url "https://files.pythonhosted.org/packages/source/r/rich/rich-13.9.4.tar.gz"
    # TODO: Update SHA256 for rich package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  resource "markdown-it-py" do
    url "https://files.pythonhosted.org/packages/source/m/markdown-it-py/markdown_it_py-3.0.0.tar.gz"
    # TODO: Update SHA256 for markdown-it-py package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  resource "mdurl" do
    url "https://files.pythonhosted.org/packages/source/m/mdurl/mdurl-0.1.2.tar.gz"
    # TODO: Update SHA256 for mdurl package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/source/p/pygments/pygments-2.18.0.tar.gz"
    # TODO: Update SHA256 for pygments package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  resource "textual" do
    url "https://files.pythonhosted.org/packages/source/t/textual/textual-0.89.1.tar.gz"
    # TODO: Update SHA256 for textual package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  resource "pyyaml" do
    url "https://files.pythonhosted.org/packages/source/p/pyyaml/pyyaml-6.0.2.tar.gz"
    # TODO: Update SHA256 for pyyaml package
    sha256 "PLACEHOLDER_UPDATE_WITH_ACTUAL_SHA256"
  end

  def install
    virtualenv_install_with_resources

    # Install shell completions
    bash_completion.install "completions/neo-says.bash" => "neo-says"
    zsh_completion.install "completions/neo-says.zsh" => "_neo-says"
    fish_completion.install "completions/neo-says.fish"
  end

  test do
    assert_match "usage", shell_output("#{bin}/neo-says --help", 0).downcase
  end
end
