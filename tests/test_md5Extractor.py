from HystrixBox.Extractors.md5_extractor import MD5Extractor

TEST = 'c7fba305d429dcda7a51e91e920b11ed asdsad sad adas dasd wqd sdwqd sad12!@#!@#@13 c@!ba305d429dcda7a51e91e920b11ed'


def test_extract():
    assert MD5Extractor.extract(TEST) == ['c7fba305d429dcda7a51e91e920b11ed']
