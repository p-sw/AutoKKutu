import sqlite3

class By:
    LOW_LENGTH = 0
    HIGH_LENGTH = 1

class DBManager:
    def __init__(self):
        self.db = sqlite3.connect('word.db')
    
    def get_word(self, by, value, dups):
        match by:
            case By.LOW_LENGTH:
                sql = f'SELECT word FROM stdict WHERE word LIKE "{value}%" ORDER BY length ASC'
            case By.HIGH_LENGTH:
                sql = f'SELECT word FROM stdict WHERE word LIKE "{value}%" ORDER BY length DESC'

        cursor = self.db.cursor()
        match_words = cursor.execute(sql).fetchall()
        for dup_word in dups:
            try:
                match_words.remove((dup_word, len(dup_word)))
            except ValueError:
                pass  # ignore if value is not exists in matched words
        return match_words
    
    def insert_word(self, word):
        cursor = self.db.cursor()
        cursor.execute('INSERT OR IGNORE INTO stdict VALUES (?, ?)', (word, len(word)))
        self.db.commit()