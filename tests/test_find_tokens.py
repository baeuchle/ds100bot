"""Unit tests for AnswerMachine.react.find_tokens"""

from AnswerMachine.react import find_tokens
from AnswerMachine.candidate import Candidate

def test_case400():
    text = 'Hallo #FF !'
    answer = [
            Candidate(('#', '', 'FF'), 'DS100'),
        ]
    result = find_tokens(text, 'none', 'DS100')
    assert answer == result

def test_case401():
    text = 'plain tags #FF #_FH #DS:FFU #DS:_FKW #DS:HG_ bot%tl%ab%ns%401'
    answer = [
            Candidate(('#', '', 'FF'), 'DS100'),
            Candidate(('#', '', '_FH'), 'DS100'),
            Candidate(('#', 'DS', 'FFU'), 'DS100'),
            Candidate(('#', 'DS', '_FKW'), 'DS100'),
            Candidate(('#', 'DS', 'HG_'), 'DS100')
        ]
    result = find_tokens(text, 'none', 'DS100')
    assert answer == result

def test_case402():
    text = 'different cases #DS:FF #DS:Fkw #ÖBB:Aa #ÖBB:AB bot%tl%xs%402'
    answer = [
            Candidate(('#', 'DS', 'FF'), 'DS100'),
            Candidate(('#', 'DS', 'Fkw'), 'DS100'),
            Candidate(('#', 'ÖBB', 'Aa'), 'DS100'),
            Candidate(('#', 'ÖBB', 'AB'), 'DS100')
        ]
    result = find_tokens(text, 'none', 'DS100')
    assert answer == result

def test_case411():
    text = 'do not find CH = Chur #_CH #BS bot%tl%ab%mt%issue13%411'
    answer = [
            Candidate(('#', '', '_CH'), '_CH'),
            Candidate(('#', '', 'BS'), '_CH')
        ]
    result = find_tokens(text, 'none', '_CH')
    assert answer == result

def test_case412():
    text = 'this works: #CH:CH'
    answer = [ Candidate(('#', 'CH', 'CH'), 'asdf') ]
    result = find_tokens(text, 'none', 'asdf')
    assert answer == result

def test_case420():
    text = 'Vol Ⅰ: #NO:249 #NO:ÅBY bot%tl%xs%unusual%420'
    answer = [
            Candidate(('#', 'NO', '249'), ""),
            Candidate(('#', 'NO', 'ÅBY'), "")
        ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case421():
    text = 'unusual tags Vol Ⅱ: $DS:VDE8¹ #CH:600133 #CH:ALT94 bot%tl%xs%unusual%421'
    answer = [
        Candidate(('$', 'DS', 'VDE8¹'), ""),
        Candidate(('#', 'CH', '600133'), ""),
        Candidate(('#', 'CH', 'ALT94'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case422():
    text = 'unusual tags Vol Ⅲ: #AT:Aa_G #AT:Aa_Z9 #AT:Z bot%tl%xs%unusual%422'
    answer = [
        Candidate(('#', 'AT', 'Aa_G'), ""),
        Candidate(('#', 'AT', 'Aa_Z9'), ""),
        Candidate(('#', 'AT', 'Z'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case423():
    text = 'unusual tags Vol Ⅳ: #DS:AA_G #DS:AAG #DS:EM302 bot%tl%xs%unusual%423'
    answer = [
        Candidate(('#', 'DS', 'AA_G'), ""),
        Candidate(('#', 'DS', 'AAG'), ""),
        Candidate(('#', 'DS', 'EM302'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case424():
    text = 'unusual tags Vol Ⅴ: #BOT:SARS_COV_2 #BOT:REKURSION #BOT:toggle bot%tl%xs%unusual%424'
    answer = [
        Candidate(('#', 'BOT', 'SARS_COV_2'), ""),
        Candidate(('#', 'BOT', 'REKURSION'), ""),
        Candidate(('#', 'BOT', 'toggle'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case425():
    text = 'unusual tags Vol Ⅵ: #HH:HX #LP:K;#LP:KA+#LP:KALD bot%tl%xs%unusual%425'
    answer = [
        Candidate(('#', 'HH', 'HX'), ""),
        Candidate(('#', 'LP', 'K'), ""),
        Candidate(('#', 'LP', 'KA'), ""),
        Candidate(('#', 'LP', 'KALD'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case426():
    text = 'un. tags Vol Ⅶ: #UK:ABE #UK:ABER #NL:Ah;#NL:Ahg/#NL:Apn #NL:APD bot%tl%xs%unusual%426'
    answer = [
        Candidate(('#', 'UK', 'ABE'), ""),
        Candidate(('#', 'UK', 'ABER'), ""),
        Candidate(('#', 'NL', 'Ah'), ""),
        Candidate(('#', 'NL', 'Ahg'), ""),
        Candidate(('#', 'NL', 'Apn'), ""),
        Candidate(('#', 'NL', 'APD'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case427():
    text = 'unusual tags Vol Ⅷ: #FR:A?#FR:AA!#FR:AAA bot%tl%xs%unusual%427'
    answer = [
        Candidate(('#', 'FR', 'A'), ""),
        Candidate(('#', 'FR', 'AA'), ""),
        Candidate(('#', 'FR', 'AAA'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case428():
    text = 'unusual tags Vol Ⅸ: $3640 #FFM:HB #FFM:_HB #FFM:211 #W:J $FFM:A3 bot%tl%xs%unusual%428'
    answer = [
        Candidate(('$', '', '3640'), ""),
        Candidate(('#', 'FFM', 'HB'), ""),
        Candidate(('#', 'FFM', '_HB'), ""),
        Candidate(('#', 'FFM', '211'), ""),
        Candidate(('#', 'W', 'J'), ""),
        Candidate(('$', 'FFM', 'A3'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case429():
    text = 'unusual tags Vol Ⅹ: $FFM:A $FFM:Aⅰ $FFM:AⅡ $FFM:AIII bot%tl%xs%unusual%429'
    answer = [
        Candidate(('$', 'FFM', 'A'), ""),
        Candidate(('$', 'FFM', 'Aⅰ'), ""),
        Candidate(('$', 'FFM', 'AⅡ'), ""),
        Candidate(('$', 'FFM', 'AIII'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case450():
    text = '#FF $1234 %Hp0 &Awanst /FFM:U2 bot%tl%sigil%450'
    answer = [
        Candidate(('#', '', 'FF'), ""),
        Candidate(('$', '', '1234'), ""),
        Candidate(('%', '', 'Hp0'), ""),
        Candidate(('&', '', 'Awanst'), ""),
        Candidate(('/', 'FFM', 'U2'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result

def test_case460():
    # both should be found, which is relevant here:
    text = 'repeated things #FF #FF'
    answer = [
        Candidate(('#', '', 'FF'), ""),
        Candidate(('#', '', 'FF'), "")
    ]
    result = find_tokens(text, 'none', '')
    assert answer == result
