import wordfinder as wd

def test_count_wf(capsys):
    wf = wd.WordFinder("python-oo-practice/words.txt")  
    captured = capsys.readouterr()
    assert captured.out == "235886 lines read\n"

def test_count_swf(capsys):
    swf = wd.SpecialWordFinder("python-oo-practice/special_words.txt")  
    captured = capsys.readouterr()
    assert captured.out == "27 lines read\n"

def test_filter_swf():
    swf = wd.SpecialWordFinder("python-oo-practice/words.txt")
    assert [w for w in swf._words if len(w.strip()) == 0 or w.startswith('#')] == []  



