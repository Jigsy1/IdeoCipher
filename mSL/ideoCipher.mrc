; Ideograph Cipher - ideoCipher.mrc - Proof of Concept by Jigsy (https://github.com/Jigsy1) released under the Unlicense.
;
; Also available in Python.
;
; How to use:
; ---------------
; //msg $chan $ideo.encode(Hello!)
; //var %string = This, is a line with $!characters mIRC % $+ doesn't #really like. | //msg $chan $ideo.encode(%string)
; //msg $chan $ideo.decode(償禮幇 凉杞釧 櫛禪滲 峻狛桶哩悸傳鳩檜裡 曉峨嶺焙祐蕪廟鮫結)
;
; Tweaking:
; ----------
; If you wish to change which number reflects what character, edit CharOrder under [Settings] in the Ideo.ini file. E.g.
;
; [Settings]
; CharOrder=!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
;
; ...becomes...
;
; [Settings]
; CharOrder=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/\()[]{}!?+-=%#"'`$&*,.:;<>@^_|~
;
; If you wish to add more characters, add the character to the end of the CharOrder under the [Settings] section and add the
; number for that character. So for example, £ onto the current charset would become 95=<ideographs>.
;
; You will need at least two ideographs because of the "no dopplegänger" code.
;
; If you want to encrypt spaces, add Space=<ideographs> under the [Key] section. Again, you will need at least two ideographs.
;
; If you want to pad the message with ideographs that have no value, add Null=<ideographs> under the [Key] section.
;
; And again, you will need at least two ideographs.

alias ideo {
  ; $ideo(<text>).<decode|encode>

  if ($prop == decode) { return $ideo.decode($1-) }
  if ($prop == encode) { return $ideo.encode($1-) }
}
alias ideo.decode {
  ; $ideo.decode(text)

  var %order = $ideo.order
  var %char = 0
  var %output = $null, %result = $null
  while (%char < $len($1-)) {
    inc %char 1
    if (($asc($mid($1-,%char,1)) == 32) || ($asc($mid($1-,%char,1)) == 160)) {
      ; `-> We need to check if the space is actually a proper space or an emulated space. Once we do that, use $chr(160) to emulate spaces since $chr(32) doesn't work well on mIRC.
      var %output = %output $+ $chr(160)
      continue
    }
    if ($read($ideo.file, w, $+(*=*,$mid($1-,%char,1),*))) {
      var %result = $gettok($v1,1,61)
      if (%result != Null) { var %output = %output $+ $iif(%result != Space,$mid(%order,%result,1),$chr(160)) }
    }
    ; `-> Otherwise, find the ideograph - assuming it isn't Null - in the file and convert it to a comprehensible value. E.g. 醉 => 77 => m
  }
  return %output
  ; `-> Return the output.
}
alias ideo.encode {
  ; $ideo.encode(text)

  var %order = $ideo.order
  var %char = 0
  var %output = $null, %last = $null, %match = $null, %ideos = $null, %current = $null
  var %padding = $iif($readini($ideo.file, Keys, Null),1,0)
  ; `-> Check to see if Null=<ideographs> are part of the *.ini file. If they're not, it won't matter. Otherwise (See: %padding)
  while (%char < $len($1-)) {
    inc %char 1
    if ($poscs(%order,$mid($1-,%char,1)) != $null) {
      ; `-> Check the character via the acceptable characters as defined above. (This is using the case-sensitive $pos identifier.)
      var %match = $v1
      ; `-> Convert the character to a number. E.g. ! = 1, " = 2, ... | = 92, etc.
      var %ideos = $removecs($readini($ideo.file, Keys, %match),%last)
      ; `-> Get all the ideographs we can use, minus the one we used last. (Won't matter if %last is $null here.)
      var %current = $mid(%ideos,$rand(1,$len(%ideos)),1)
      ; `-> Now get a random ideograph from the ones we can use.
      var %output = %output $+ %current
      ; `-> And then add it to the output string.
      var %last = %current
      ; ¦-> Set the last ideograph to the new ideograph.
      ; ¦-> This reason for this is to make sure the ideograph can never be used again in succession. For example, Grrr => 貌よ一よ is acceptable, whilst Grrr => 貌よよよ is not.
      ; `-> Having the same ideograph after a space as the last ideograph before a space is also acceptable. E.g. Grrr r => 貌よ一よ よ
      if (%padding != 1) { continue }
      ; ,-> This means Null=... is part of the *.ini file. Now we just need to check if we should pad the letter with a bonus ideograph.
      if ($rand(1,$ideo.null.chance.1) >= $int($calc($ideo.null.chance.1 / $ideo.null.chance.2))) {
        ; `-> The "variables" for these are at the bottom. But if you want to modify the $calc(...) feel free.
        var %ideos = $removecs($readini($ideo.file, Keys, Null),%last)
        var %current = $mid(%ideos,$rand(1,$len(%ideos)),1)
        var %output = %output $+ %current
        var %last = %current
      }
      continue
    }
    if ($asc($mid($1-,%char,1)) == 32) {
      ; `-> Check to see if Space=... exists in the *.ini file. If it does, do the exact same as above. Otherwise...
      if ($readini($ideo.file, Keys, Space) == $null) {
        ; `-> Use $chr(160) to emulate spaces since $chr(32) doesn't work well on mIRC. Also set the last ideograph to $null.
        var %output = %output $+ $chr(160), %last = $null
      }
      ; >-> I simply didn't want to set a flag to skip this check so I'm checking it twice.
      if ($readini($ideo.file, Keys, Space) != $null) {
        var %ideos = $removecs($v1,%last)
        var %current = $mid(%ideos,$rand(1,$len(%ideos)),1)
        var %output = %output $+ %current
        var %last = %current
      }
      if (%padding != 1) { continue }
      if ($rand(1,$ideo.null.chance.1) >= $int($calc($ideo.null.chance.1 / $ideo.null.chance.2))) {
        var %ideos = $removecs($readini($ideo.file, Keys, Null),%last)
        var %current = $mid(%ideos,$rand(1,$len(%ideos)),1)
        var %output = %output $+ %current
        var %last = %current
      }
      continue
    }
    return
    ; `-> Having an erroneous character is a flaw.
  }
  return %output
  ; `-> Return the output.
}
alias -l ideo.file { return $qt($scriptdirIdeo.ini) }
; `-> If the file is in a different folder or whatever, change this.
alias -l ideo.null.chance.1 { return 100000 }
alias -l ideo.null.chance.2 { return 1.29 }
; `-> For calculating how many times a null character should appear. Feel free to change these.
alias -l ideo.order { return $readini($ideo.file, n, Settings, CharOrder) }
; ¦-> The only acceptable characters that can be encoded. If you would like to add more like ö or £, for example, you can, but the *.ini file will need updating to reflect this.
; `-> So if you add ö onto the end of the [Settings]->CharOrder=...}~, you will need to add 95=<some ideographs go here> to the *.ini file.

; EOF
