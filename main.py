class CodeBlockCaptureIter:
    OPEN = "```json"
    CLOSE = "```"

    def __init__(self, it):
        self.src = iter(it)
        self.code_block = None

    def __iter__(self):
        return self

    def __next__(self):
        next_value = next(self.src)
        open_ptr = 0
        next_value_ptr = next_value.find(self.OPEN[open_ptr])

        if next_value_ptr != -1:
            code_block_start_idx = -1
            code_block_end_idx = -1
            while True:
                open_ptr += 1
                next_value_ptr += 1

                # If next_value is not long enough to contain whole opening string we get next chunks as until it fits ...
                while next_value_ptr >= len(next_value):
                    next_value += next(self.src)

                # We still did not see all of the opening string ...
                if open_ptr < len(self.OPEN):
                    # print(f"next_value[{next_value_ptr}]: '{next_value[next_value_ptr]}' | self.OPEN[{open_ptr}]: {self.OPEN[open_ptr]}")
                    if next_value[next_value_ptr] == self.OPEN[open_ptr]:
                        continue

                # Now we actually saw all of the opening ...
                else:
                    code_block_start_idx = next_value_ptr
                    # Let's see if we go on and see the closing string in the stream ...
                    close_ptr = 0
                    while True:
                        # If next ...
                        while next_value_ptr >= len(next_value):
                            next_value += next(self.src)
                        if next_value[next_value_ptr] == self.CLOSE[0]:
                            # We found the potential first character of the closing string ...
                            close_ptr += 1
                            code_block_end_idx = next_value_ptr
                            break;
                        else:
                            # We did not see the first character of the closing string so we move on ...
                            next_value_ptr += 1

                    # Let's see if we can find the whole closing string now ...
                    while True:
                        # If next ...
                        while next_value_ptr >= len(next_value):
                            next_value += next(self.src)
                        if close_ptr < len(self.CLOSE):
                            # print(f"next_value[{next_value_ptr}]: '{next_value[next_value_ptr]}' | self.CLOSE[{close_ptr}]: {self.CLOSE[close_ptr]}")
                            if next_value[next_value_ptr] == self.CLOSE[close_ptr]:
                                close_ptr += 1
                                next_value_ptr += 1
                                continue
                        else:
                            # Seems like we found the whole closing string as well ...
                            self.code_block = next_value[code_block_start_idx:code_block_end_idx].replace("\n", "")
                            return next_value[:code_block_start_idx - len(self.OPEN)] + next_value[code_block_end_idx + len(self.CLOSE):]
                    break


        return next_value

def test_iter():
    chunks = [
        "Hell","o Wo","rld!","\n``","`jso","n\n{","\"fo","o\":"," \"b","ar\"","}\n`","``\nblub"
    ]

    code_block_iter = CodeBlockCaptureIter(iter(chunks))

    result = "".join([f for f in code_block_iter]).replace("\n", "")
    code_block = code_block_iter.code_block

    assert "Hello World!blub" == result
    assert "{\"foo\": \"bar\"}" == code_block
