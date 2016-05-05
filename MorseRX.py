# Module MorseRX
# decodes the received morse code tuples
from MorseCode import MorseCode
import MorseTX

def MorseRX(readings):
    # Decoded the readings received as tuples (state, duration)
    # Readings may be a generator
    morse_letter = "" # current letter that is being formed
    decoded = ""
    morse_letter = ''

    for voltage, duration in readings:
        #print('({0},{1})'.format(voltage, duration))
        if voltage:
            if duration == 1:
                morse_letter += '.'
            elif duration == 3:
                morse_letter += '-'
        #    print(morse_letter)
        else:
            if duration >= 3:
                # Must include greater than duration because will not otherwise convert
                # the morse letter on hold and will skip to a space
                decoded += get_letter(morse_letter)
                morse_letter = ''
            if duration < 8 and duration >= 7:
                decoded += ' '
    return decoded

def get_letter(morse):
    for l, m in MorseCode.items():
        if m == morse:
            return l
    # If didn't find a match for the morse, something went wrong...
    return '#'

if __name__ == "__main__":
    print(MorseRX([(1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (0, 3),
        (1, 1), (0, 1), (1, 1), (0, 7),
        (1, 1), (0, 1), (1, 3), (0, 1), (1, 3), (0, 1), (1, 1), (0, 3),
        (1, 1), (0, 1), (1, 1), (0, 7),
        (1, 3), (0, 1), (1, 1), (0, 1), (1, 1), (0, 1), (1, 1), (0, 3),
        (1, 1), (0, 1), (1, 1), (0, 8)]))