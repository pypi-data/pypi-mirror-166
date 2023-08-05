import sys, os, re, codecs, time, copy, traceback
from pcpp.parser import STRING_TYPES, default_lexer, trigraph, Macro, Action, OutputDirective, PreprocessorHooks
from pcpp.evaluator import Evaluator

from pcpp.preprocessor import Preprocessor as PCPP_Preprocessor
from pcpp.ply.ply.lex import LexToken

# Some Python 3 compatibility shims
if sys.version_info.major < 3:
    FILE_TYPES = file
    clock = time.clock
else:
    xrange = range
    import io
    FILE_TYPES = io.IOBase
    clock = time.process_time


class Preprocessor(PCPP_Preprocessor):
    def expand_macros(self,tokens,expanding_from=[]):
        """Given a list of tokens, this function performs macro expansion."""
        # Each token needs to track from which macros it has been expanded from to prevent recursion
        # for tok in tokens:
        #     if not hasattr(tok, 'expanded_from'):
        #         tok.expanded_from = []
        # i = 0
        # #print("*** EXPAND MACROS in", "".join([t.value for t in tokens]), "expanding_from=", expanding_from)
        # #print(tokens)
        # #print([(t.value, t.expanded_from) for t in tokens])
        # while i < len(tokens):
        #     t = tokens[i]
        #     if self.linemacrodepth == 0:
        #         self.linemacro = t.lineno
        #     self.linemacrodepth = self.linemacrodepth + 1
        #     if t.type == self.t_ID:
        #         if t.value in self.macros and t.value not in t.expanded_from and t.value not in expanding_from:
        #             # Yes, we found a macro match
        #             m = self.macros[t.value]
        #             if m.arglist is None:
        #                 # A simple macro
        #                 rep = [copy.copy(_x) for _x in m.value]
        #                 ex = self.expand_macros(rep, expanding_from + [t.value])
        #                 #print("\nExpanding macro", m, "\ninto", ex, "\nreplacing", tokens[i:i+1])
        #                 for e in ex:
        #                     e.source = t.source
        #                     e.lineno = t.lineno
        #                     if not hasattr(e, 'expanded_from'):
        #                         e.expanded_from = []
        #                     e.expanded_from.append(t.value)
        #                     ref = t.value
        #                     expansion = f'{ref} ⟹'
        #                     expansion_comment = f'/* {expansion} */'
        #                     ws_tok = LexToken()
        #                     ws_tok.type = self.t_SPACE
        #                     ws_tok.value = ' '
        #                     ws_tok.lineno = ex[0].lineno
        #                     ws_tok.lexpos = ex[0].lexpos
        #                     ws_tok.source = ex[0].source
        #                     ws_tok_after = LexToken()
        #                     ws_tok_after.type = self.t_SPACE
        #                     ws_tok_after.value = ' '
        #                     ws_tok_after.lineno = ex[0].lineno
        #                     ws_tok_after.lexpos = ex[0].lexpos
        #                     ws_tok_after.source = ex[0].source
        #                     subst_comment_tok = LexToken()
        #                     subst_comment_tok.type = self.t_COMMENT1
        #                     subst_comment_tok.value = expansion_comment
        #                     subst_comment_tok.lineno = ex[0].lineno
        #                     subst_comment_tok.lexpos = ex[0].lexpos
        #                     subst_comment_tok.source = ex[0].source
        #                 tokens[i:i+1] = [ws_tok, subst_comment_tok, ws_tok_after] + ex
        #             else:
        #                 # A macro with arguments
        #                 j = i + 1
        #                 while j < len(tokens) and (tokens[j].type in self.t_WS or tokens[j].type in self.t_COMMENT):
        #                     j += 1
        #                 # A function like macro without an invocation list is to be ignored
        #                 if j == len(tokens) or tokens[j].value != '(':
        #                     i = j
        #                 else:
        #                     tokcount,args,positions = self.collect_args(tokens[j:], True)
        #                     if tokcount == 0:
        #                         # Unclosed parameter list, just bail out
        #                         break
        #                     if (not m.variadic
        #                         # A no arg or single arg consuming macro is permitted to be expanded with nothing
        #                         and (args != [[]] or len(m.arglist) > 1)
        #                         and len(args) !=  len(m.arglist)):
        #                         self.on_error(t.source,t.lineno,"Macro %s requires %d arguments but was passed %d" % (t.value,len(m.arglist),len(args)))
        #                         i = j + tokcount
        #                     elif m.variadic and len(args) < len(m.arglist)-1:
        #                         if len(m.arglist) > 2:
        #                             self.on_error(t.source,t.lineno,"Macro %s must have at least %d arguments" % (t.value, len(m.arglist)-1))
        #                         else:
        #                             self.on_error(t.source,t.lineno,"Macro %s must have at least %d argument" % (t.value, len(m.arglist)-1))
        #                         i = j + tokcount
        #                     else:
        #                         if m.variadic:
        #                             if len(args) == len(m.arglist)-1:
        #                                 args.append([])
        #                             else:
        #                                 args[len(m.arglist)-1] = tokens[j+positions[len(m.arglist)-1]:j+tokcount-1]
        #                                 del args[len(m.arglist):]
        #                         else:
        #                             # If we called a single arg macro with empty, fake extend args
        #                             while len(args) < len(m.arglist):
        #                                 args.append([])

        #                         # Get macro replacement text
        #                         rep = self.macro_expand_args(m,args)
        #                         ex = self.expand_macros(rep, expanding_from + [t.value])
        #                         for e in ex:
        #                             e.source = t.source
        #                             e.lineno = t.lineno
        #                             if not hasattr(e, 'expanded_from'):
        #                                 e.expanded_from = []
        #                             e.expanded_from.append(t.value)
        #                         # A non-conforming extension implemented by the GCC and clang preprocessors
        #                         # is that an expansion of a macro with arguments where the following token is
        #                         # an identifier inserts a space between the expansion and the identifier. This
        #                         # differs from Boost.Wave incidentally (see https://github.com/ned14/pcpp/issues/29)
        #                         if len(tokens) > j+tokcount and tokens[j+tokcount].type in self.t_ID:
        #                             #print("*** token after expansion is", tokens[j+tokcount])
        #                             newtok = copy.copy(tokens[j+tokcount])
        #                             newtok.type = self.t_SPACE
        #                             newtok.value = ' '
        #                             ex.append(newtok)
        #                         #print("\nExpanding macro", m, "\n\ninto", ex, "\n\nreplacing", tokens[i:j+tokcount])
        #                         ref = t.value
        #                         subst = ''.join(tt.value for tt in ex)
        #                         expansion = f'{ref} ⟹'
        #                         expansion_comment = f'/* {expansion} */'
        #                         ws_tok = LexToken()
        #                         ws_tok.type = self.t_SPACE
        #                         ws_tok.value = ' '
        #                         ws_tok.lineno = ex[0].lineno
        #                         ws_tok.lexpos = ex[0].lexpos
        #                         ws_tok.source = ex[0].source
        #                         ws_tok_after = LexToken()
        #                         ws_tok_after.type = self.t_SPACE
        #                         ws_tok_after.value = ' '
        #                         ws_tok_after.lineno = ex[0].lineno
        #                         ws_tok_after.lexpos = ex[0].lexpos
        #                         ws_tok_after.source = ex[0].source
        #                         subst_comment_tok = LexToken()
        #                         subst_comment_tok.type = self.t_COMMENT1
        #                         subst_comment_tok.value = expansion_comment
        #                         subst_comment_tok.lineno = ex[0].lineno
        #                         subst_comment_tok.lexpos = ex[0].lexpos
        #                         subst_comment_tok.source = ex[0].source
        #                         tokens[i:j+tokcount] = [ws_tok, subst_comment_tok, ws_tok_after] + ex
        #             self.linemacrodepth = self.linemacrodepth - 1
        #             if self.linemacrodepth == 0:
        #                 self.linemacro = 0
        #             continue
        #         elif self.expand_linemacro and t.value == '__LINE__':
        #             t.type = self.t_INTEGER
        #             t.value = self.t_INTEGER_TYPE(self.linemacro)
        #         elif self.expand_countermacro and t.value == '__COUNTER__':
        #             t.type = self.t_INTEGER
        #             t.value = self.t_INTEGER_TYPE(self.countermacro)
        #             self.countermacro += 1

        #     i += 1
        #     self.linemacrodepth = self.linemacrodepth - 1
        #     if self.linemacrodepth == 0:
        #         self.linemacro = 0
        return tokens
