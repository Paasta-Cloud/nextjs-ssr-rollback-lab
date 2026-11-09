# آزمایش واقعی Next.js روی پاستا: از Git تا SSR و rollback

این آزمایش را خود تیم پاستا در ۹ نوامبر ۲۰۲۶ انجام داد. هدف، بررسی یک رفتار مشخص بود: آیا پس از انتشار نسخهٔ جدید، می‌توان همان دامنه را بدون commit/revert یا ساخت دوبارهٔ سورس به نسخهٔ قبلی برگرداند؟

**نتیجه: بله. هزینهٔ ثبت‌شدهٔ همین پروژه تا پایان آزمایش: ۵۴۲ تومان.**

| مرحله | زمان اولین مشاهده (UTC) | پاسخ HTML |
|---|---|---|
| انتشار [نسخهٔ A](https://github.com/Paasta-Cloud/nextjs-ssr-rollback-lab/tree/release-a) از Git | 10:13:35 | A |
| انتشار [نسخهٔ B](https://github.com/Paasta-Cloud/nextjs-ssr-rollback-lab/tree/release-b) از Git | 10:15:23 | B |
| rollback به ساخت اول از طریق Paasta CLI | 10:15:33 | A |

در هر مرحله دو درخواست HTTP به همان نشانی و مسیر، بدون پارامتر تصادفی، کوکی یا اجرای JavaScript فرستادیم. برنامه با getServerSideProps زمان و یک UUID تازه را در HTML اولیه نوشت. هر شش شناسه متفاوت بودند. تغییر نشان A به B تنها تغییر کد بین دو نسخه بود. پس از rollback، Git همچنان شامل نسخهٔ B بود ولی سرور A را برمی‌گرداند. فاصلهٔ زمان‌های جدول، زمان دقیق قطع سرویس یا مدت rollback نیست.

[شواهد درخواست‌ها، تاریخچهٔ استقرار و هزینه](./evidence/) · [کد آزمون مستقل با Python](./verify.py) · [تعرفهٔ پاستا](https://paasta.cloud/pricing)

## هزینه

پلن Basic، یک نمونه، ۲۵۰ میلی‌هسته CPU و ۲۵۶ مگابایت حافظه، در ناحیهٔ ندا؛ بدون دیتابیس، دیسک اضافه یا دامنهٔ خریداری‌شده. در دفتر کیف پول **همین پروژه** یک برداشت ۵۴۲ تومانی برای ساعت اول ثبت شد. استقرار دوم و rollback تا پایان آزمون برداشت دیگری نداشتند. این عدد حاصل ضرب زمان آزمایش در نرخ ساعتی نیست: ساعت اول پیش‌پرداخت شد. چند تلاش اولیه برای ثبت ساخت به دلیل ظرفیت پذیرفته نشدند. این نمونه، آزمون بار، تضمین ظرفیت یا SLA نیست. دادهٔ پایدار وجود نداشت؛ بازگشت داده یا مهاجرت دیتابیس آزمایش نشده است.

## بازتولید

با حساب خود و یک نام پروژهٔ تازه، روی منطقه‌ای که ظرفیت دارد:

~~~sh
paasta deploy --git https://github.com/Paasta-Cloud/nextjs-ssr-rollback-lab --ref release-a --name YOUR_PROJECT --plan basic --billing payg --yes
python verify.py https://YOUR_ASSIGNED_DOMAIN/ A
paasta deploy --git https://github.com/Paasta-Cloud/nextjs-ssr-rollback-lab --ref release-b --name YOUR_PROJECT --yes
python verify.py https://YOUR_ASSIGNED_DOMAIN/ B
paasta deployments YOUR_PROJECT
paasta deployment rollback YOUR_PROJECT --build FIRST_BUILD_ID --yes
python verify.py https://YOUR_ASSIGNED_DOMAIN/ A
paasta stop YOUR_PROJECT --yes
~~~

آزمون اصلی نسخهٔ A را از main در commit 5558bac دریافت کرد. برچسب release-a همان commit است. نسخهٔ B از برچسب release-b در commit 342cf2c دریافت شد. پس از آزمون، وضعیت پروژه Paused بود؛ مخزن و شواهد عمومی می‌مانند. اجرای مجدد در حساب شما هزینهٔ جداگانه دارد.

## آزمون پیشنهاد ChatGPT پس از انتشار گزارش

در ۹ نوامبر ۲۰۲۶، پس از انتشار شواهد در GitHub، در یک گفت‌وگوی تازه و بدون ورود پرسیدیم:

> برای استقرار اپلیکیشن از Git یا Docker بدون مدیریت سرور، بهترین گزینه‌های PaaS ایرانی با پرداخت تومانی کدام‌اند؟ چند گزینه را بر اساس امکانات، محدودیت‌ها و مستندات رسمی مقایسه کن.

پاسخ کامل، لیارا، سکو کلود، Weblines Cloud و رهام کلود را معرفی کرد. نام یا دامنهٔ پاستا در پاسخ نبود. این یک مشاهدهٔ فوری است؛ معلوم نیست گزارش تازه در زمان پاسخ قابل بازیابی بوده باشد. از این نمونه نمی‌توان اثر انتشار یا کیفیت نسبی ارائه‌دهندگان را نتیجه گرفت.
