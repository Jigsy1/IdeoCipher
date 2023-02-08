; Ideograph Cipher - Proof of Concept by Jigsy.
;
; Written in mIRC script because I don't really know any other programming languages (yet) to demonstrate the concept.
;
; How to use:
; -----------
; //msg $chan $ideo.encode(Hello!)
; //var %t = This, is a line with $!characters mIRC % $+ doesn't really like. | //msg $chan $ideo.encode(%t)
; //msg $chan $ideo.decode(償禮幇 凉杞釧 櫛禪滲 峻狛桶哩悸傳鳩檜裡 曉峨嶺焙祐蕪廟鮫結)
;
; Tweaking:
; ---------
; If you wish to change which number reflects what character, edit CharOrder under [Settings]. E.g.
;
; [Settings]
; CharOrder=!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
;
; ...becomes...
;
; [Settings]
; CharOrder=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/\()[]{}!?+-=%#"'`$&*,.:;<>@^_|~
;
; If you wish to add more characters, add the character to the end of the CharOrder under the [Settings] section and add the number for that character. So for example, £ onto the current charset would become 95=<ideographs>.
; You will need at least two ideographs because of the "no dopplegänger" code.
;
; If you want to encrypt spaces, add Space=<ideographs> under the [Key] section. Again, you will need at least two ideographs.
;
; If you want to pad the message with ideographs that have no value, add Null=<ideographs> under the [Key] section. And again, you will need at least two ideographs.

alias ideo.decode {
  ; $ideo.decode(text)

  var %0 = $ideo.order
  var %1 = 0
  var %2, %3
  while (%1 < $len($1-)) {
    inc %1
    if (($asc($mid($1-,%1,1)) == 32) || ($asc($mid($1-,%1,1)) == 160)) { var %2 = %2 $+ $chr(160) }
    ; `-> We need to check if the space is actually a proper space or an emulated space. Once we do that, use $chr(160) to emulate spaces since $chr(32) doesn't work well on mIRC.
    else {
      if ($read($ideo.file, w, $+(*=*,$mid($1-,%1,1),*))) {
        var %3 = $gettok($v1,1,61)
        if (%3 != Null) { var %2 = %2 $+ $iif(%3 != Space,$mid(%0,%3,1),$chr(160)) }
      }
      ; `-> Otherwise, find the ideograph in the file and convert it to a comprehensible value. E.g. 醉 => 77 => m
    }
  }
  return %2
  ; `-> Return the output.
}
alias ideo.encode {
  ; $ideo.encode(text)

  var %0 = $ideo.order
  var %1 = 0
  var %2, %3, %4, %5, %6
  var %7 = $iif($readini($ideo.file, Keys, Null),1,0)
  ; `-> Check to see if Null=<ideographs> are part of the *.ini file. If they're not, it won't matter. Otherwise (See: %7)
  while (%1 < $len($1-)) {
    inc %1
    if ($poscs(%0,$mid($1-,%1,1))) {
      ; `-> Check the character via the acceptable characters as defined above. (This is using the case-sensitive $pos identifier.)
      var %4 = $v1
      ; `-> Convert the character to a number. E.g. ! = 1, " = 2, ... | = 92, etc.
      var %5 = $removecs($readini($ideo.file, Keys, %4),%3)
      ; `-> Get all the ideographs we can use, minus the one we used last. (Won't matter if %3 is $null here.)
      var %6 = $mid(%5,$rand(1,$len(%5)),1)
      ; `-> Now get a random ideograph from the ones we can use.
      var %2 = %2 $+ %6
      ; `-> And then add it to the output string.
      var %3 = %6
      ; `-> Set the last ideograph to the new ideograph.
      ;     This reason for this is to make sure the ideograph can never be used again in succession. For example, Grrr => 貌よ一よ is acceptable, whilst Grrr => 貌よよよ is not.
      ;     Having the same ideograph after a space as the last ideograph before a space is also acceptable. E.g. Grrr r => 貌よ一よ よ
      if (%7 == 1) {
        ; `-> This means Null=... is part of the *.ini file. Now we just need to check if we should pad the letter with a bonus ideograph.
        if ($rand(1,$ideo.null.chance.1) >= $int($calc($ideo.null.chance.1 / $ideo.null.chance.2))) {
          ; `-> The "variables" for these are at the bottom. But if you want to modify the $calc(...) feel free.
          var %5 = $removecs($readini($ideo.file, Keys, Null),%3)
          var %6 = $mid(%5,$rand(1,$len(%5)),1)
          var %2 = %2 $+ %6
          var %3 = %6
        }
      }
    }
    else {
      if ($asc($mid($1-,%1,1)) == 32) {
        if ($readini($ideo.file, Keys, Space)) {
          ; `-> Check to see if Space=... exists in the *.ini file. If it does, do the exact same as above. Otherwise...
          var %5 = $removecs($v1,%3)
          var %6 = $mid(%5,$rand(1,$len(%5)),1)
          var %2 = %2 $+ %6
          var %3 = %6
        }
        else { var %2 = %2 $+ $chr(160), %3 = $null }
        ; `-> Use $chr(160) to emulate spaces since $chr(32) doesn't work well on mIRC. Also set the last ideograph to $null.
        if (%7 == 1) {
          if ($rand(1,$ideo.null.chance.1) >= $int($calc($ideo.null.chance.1 / $ideo.null.chance.2))) {
            var %5 = $removecs($readini($ideo.file, Keys, Null),%3)
            var %6 = $mid(%5,$rand(1,$len(%5)),1)
            var %2 = %2 $+ %6
            var %3 = %6
          }
        }
        ; `-> This should hopefully work after the else. It's either this or having the same code twice. (Which would probably be a more sensisble solution.)
      }
      else { return }
      ; `-> I've decided to change this. Yes, I know, it sucks. But I felt that having an erroneous character was a flaw; and there's no real way of decoding the X back
      ;     to it's regular character unless I manage to come up with such a method. Until then, all messages are strict, and you'll need to either write the character
      ;     as a word (like pounds), or add the character into the *.ini file. (Which you'd probably do if you shared it with somebody anyway.)
    }
  }
  return %2
  ; `-> Return the output.
}
alias -l ideo.file { return $qt($scriptdirIdeo.ini) }
; `-> If the file is in a different folder or whatever, change this.
alias -l ideo.null.chance.1 { return 100000 }
alias -l ideo.null.chance.2 { return 1.29 }
; `-> For calculating how many times a null character should appear. Feel free to change these.
alias -l ideo.order { return $readini($ideo.file, n, Settings, CharOrder) }
; `-> The only acceptable characters that can be encoded. If you would like to add more like ö or £, for example, you can, but the *.ini file will need updating to reflect this.
;     So if you add ö onto the end of the [Settings]->CharOrder=...}~, you will need to add 95=<some ideographs go here> to the *.ini file.

; EOF
