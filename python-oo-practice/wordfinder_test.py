import wordfinder as wd

def test_count(capsys):
    w = wd.WordFinder("python-oo-practice/words.txt")  
    captured = capsys.readouterr()
    assert captured.out == "235886 lines read\n"





