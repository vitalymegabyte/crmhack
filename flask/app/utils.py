from os import name
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def normal_form(word):
    return morph.parse(word)[0].normal_form

def normalize_text(text):
    text_beaten = text.split(' ')
    text_normalized = list(map(normal_form, text_beaten))
    return text_normalized

def lemmatize_text(text):
    return ' '.join(normalize_text(text))

#объект должен иметь поле normalized_name
def getObjectsFromText(text, all_objects):
    dict_of_objects = dict(map(lambda obj: (obj.normalized_name, obj), all_objects))
    normalized_text = normalize_text(text)
    objects_to_return = []
    for i in range(1, len(normalized_text)):
        for j in range(len(normalized_text) - i + 1):
            name_done = ' '.join(normalized_text[j:j+i])
            if name_done in dict_of_objects:
                objects_to_return.append(dict_of_objects[name_done])
    return objects_to_return