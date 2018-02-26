import pytest


def numbers_from_string(number_string):
    if number_string:
        delim = ','
        delimeters = []
        if len(number_string) > 1 and number_string[:2] == '//':
            if number_string[2] == '[':
                if number_string.count("[") > 1:
                    roi = number_string[number_string.find("["):number_string.rfind("]")+1]
                    number_string = number_string.replace("//{}".format(roi), '')
                    while roi.count("[") > 0:
                        current = roi[roi.find("[")+1:roi.find("]")]
                        roi = roi.replace('[{}]'.format(current), '')
                        delimeters.append(current)
                else:
                    delim = number_string[number_string.find("[")+1:number_string.find("]")]
                    number_string = number_string[(4+len(delim)):]
            else:
                delim = number_string[2]
                number_string = number_string[2:]
        if delimeters:
            for delim in delimeters:
                number_string = number_string.replace(delim, ',')
            return handle_delimeter(number_string, ',')
        else:
            return handle_delimeter(number_string, delim)
    else:
        return 0


def handle_delimeter(number_string, delim):
    my_list = [i.split("\n") for i in number_string.split(delim)]
    flat_list = [item for sublist in my_list for item in sublist]
    for i in flat_list:
        converted = int(i or 0)
        if converted < 0:
            raise SyntaxError("Negatives not allowed! " + i)
        if converted > 1000:
            flat_list.remove(str(converted))
    numbers_list = [int(i or 0) for i in flat_list]
    return sum(numbers_list)


def test_empty_string():
    assert 0 == numbers_from_string("")


def test_one_nonempty_string():
    assert 1 == numbers_from_string("1")


def test_two_nonempty_strings():
    assert 3 == numbers_from_string("1,2")


def test_newlines():
    assert 9 == numbers_from_string("2\n4,3\n")


def test_delimeters():
    assert 3 == numbers_from_string("//;1;2")


def test_delimeters_with_newlines():
    assert 3 == numbers_from_string("//;\n1\n;2")


def test_negatives_not_allowed():
    with pytest.raises(SyntaxError, match="Negatives not allowed!"):
        numbers_from_string("-2,3")


def test_numbers_bigger_than_thousand_ignored():
    assert 2 == numbers_from_string("1001,2")


def test_longer_delimeters():
    assert 3 == numbers_from_string("//[****]\n1\n****2")


def test_multiple_delimeters():
    assert 6 == numbers_from_string("//[*][%][^]\n1\n*2%3")


def test_multiple_and_longer_delimeters():
    assert 6 == numbers_from_string("//[**][%%%][^]\n1\n**2%%%3")
