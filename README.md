# תיק עבודות

Noam Meroz. הדברים כאן רצים, ויש להם בדיקה או אתר.

## משחקים

### [BloomGrid](https://github.com/noam2177/bloomgrid)

פאזל בלוקים ב-Godot. לוח 8×8, שלושה חלקים, שורה או עמודה מלאה מתנקה. שורה ועמודה באותו מהלך הן סופרנובה.

החוקים יושבים ב-`core/`, בלי ציור ובלי קלט, כדי שאפשר לבדוק הנחה וניקוי בלי לפתוח חלון. `game/` מצייר וגורר. עדיין לא בחנות. יש גם מצב Race עם שעון.

### [טורניר Clash](https://github.com/noam2177/coc-tournament)

אתר הרשמה לטורניר: טופס, ברקט, צ'ק-אין, וארכיון. האתר שרץ: [coc-tournament.lovable.app](https://coc-tournament.lovable.app).

הנתונים ב-Supabase. הרשמה ציבורית נספרת בנפרד ממסך האדמין. זה לא אותו מוצר כמו שיתוף הבסיסים.

### [CoCLZ](https://github.com/noam2177/coclz-connect)

אתר נפרד לשיתוף בסיסים וצבאות, עם פרופיל ופיד. הטורניר רק מפנה אליו. הקוד לא יושב באותו ריפו.

## מוצר

### [הזמנות RSVP](https://github.com/noam2177/danielntomerafter)

רשימת אורחים חיה ואחוז מענה. דף אורח עם טוקן, ופאנל עם מגיעים, לא מגיעים, וללא מענה. התשובה בוואטסאפ היא מכונת מצבים על מספר, והבדיקות לא שולחות הודעה מהמעבדה.

## מעקב משרות

### [job-board](https://github.com/noam2177/job-board)

קובץ JSON מקומי הופך לעמוד HTML אחד.

העמוד סופר כמה משרות פתוחות וכמה כבר נשלחו, ומאחד כתובות כפולות לטבלת מקורות. הוא לא שולח מייל. הקובץ שבריפו הוא דוגמה מומצאת, בלי חברות אמיתיות ובלי קורות חיים.

```text
python board.py
```

## ניתוח

| ריפו | מה בודקים |
| --- | --- |
| [tfidf-rank](https://github.com/noam2177/tfidf-rank) | קוסינוס TF-IDF מול Jaccard |
| [he-segment](https://github.com/noam2177/he-segment) | שלוש מערכות על מבחן קפוא: בייסליין, לקסיקון, מודל תווים |
| [he-nlp](https://github.com/noam2177/he-nlp) | תחילית עברית, ואם אחריה באה ה׳ הידיעה גם אותה |
| [anscombe-check](https://github.com/noam2177/anscombe-check) | אותו סיכום לארבע צורות, והשארית הגדולה מהקו |
| [csv-sum](https://github.com/noam2177/csv-sum) | ספירת שורות, סכום, וממוצע |
| [bracket-check](https://github.com/noam2177/bracket-check) | סוגריים עגולים ומרובעים בזוג |
