import sys
from sly import Lexer


class FloLexer(Lexer):
    # Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
    tokens = {
        IDENTIFIANT,
        TYPE,
        INTEGER,
        BOOLEAN,
        IF,
        ELSE,
        WHILE,
        RETURN,
        AND,
        OR,
        NOT,
        EQ,
        LE,
        GE,
        NE,
    }

    # Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale.
    # Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
    # Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
    literals = {"+", "-", "*", "/", "%", "(", ")", ";", ",", "{", "}", "=", ">", "<"}

    # chaines contenant les caractère à ignorer. Ici espace et tabulation
    ignore = " \t"

    # Expressions régulières correspondant au différents Lexèmes par ordre de priorité
    EQ = r"=="
    LE = r"<="
    GE = r">="
    NE = r"!="

    @_(r"0|[1-9][0-9]*")
    def INTEGER(self, t):
        t.value = int(t.value)
        return t

    @_(r"Vrai|Faux")
    def BOOLEAN(self, t):
        t.value = t.value == "Vrai"
        return t

        # cas général

    IDENTIFIANT = r"[a-zA-Z][a-zA-Z0-9_]*"  # en général, variable.flo ou nom de fonction

    # cas spéciaux:
    IDENTIFIANT["booleen"] = TYPE
    IDENTIFIANT["entier"] = TYPE
    IDENTIFIANT["si"] = IF
    IDENTIFIANT["sinon"] = ELSE
    IDENTIFIANT["tantque"] = WHILE
    IDENTIFIANT["retourner"] = RETURN
    IDENTIFIANT["et"] = AND
    IDENTIFIANT["ou"] = OR
    IDENTIFIANT["non"] = NOT

    # Syntaxe des commentaires à ignorer
    ignore_comment = r"\#.*"

    # Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    # En cas d'erreur, indique où elle se trouve
    def error(self, t):
        print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"', file=sys.stderr)
        self.index += 1
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)
