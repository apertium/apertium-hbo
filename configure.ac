AC_PREREQ(2.52)

AC_INIT([Apertium Ancient Hebrew], [0.1.0], [popcorn.tomato.dude@gmail.com], [apertium-hbo], [https://wiki.apertium.org/wiki/Apertium-hbo])
AM_INIT_AUTOMAKE
AC_PROG_AWK

PKG_CHECK_MODULES(APERTIUM, apertium >= 3.8.0)
PKG_CHECK_MODULES(HFST, hfst >= 3.15.1)
PKG_CHECK_MODULES(CG3, cg3 >= 1.3.1)
PKG_CHECK_MODULES(LEXD, lexd >= 1.1.0)

PKG_CHECK_MODULES(HFSTOSPELL, hfstospell >= 0.2, [], [
      AC_MSG_NOTICE([You will need hfst-ospell installed to use the compiled speller])
])

PKG_CHECK_MODULES(REGTEST, apertium-regtest >= 0.0.1, [], [
      AC_MSG_WARN([Running tests requires apertium-regtest])
])

AP_MKINCLUDE

AC_OUTPUT([Makefile apertium-hbo.pc])
