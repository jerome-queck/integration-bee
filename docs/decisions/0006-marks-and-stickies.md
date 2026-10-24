# Marks and stickies

`turn apply` writes both files. A correct mark with `extract.method_note` stores `answer_ok` true and `method_ok` false, and replaces that technique's card. A correct mark without the note stores `method_ok` true. A wrong final answer does not guess the method. A repeat of the same answer while the problem is still open does not append another attempt. Strength is computed from the touched day and is not stored.

There is no second mark command. Attempts and the journal stay as they are.
