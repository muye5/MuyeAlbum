Description
=========
personal web album

    crawl images from web(www.sina.com.cn for example)  
    
    store image urls into a database, url filtered by python bloomfilter  
    
    add crawled images your web album

Environment & Tools
=========

    0. Ubuntu11.10

    1. Apache2

    2. MySQL5.0

    3. Scrapy

    4. Gallery2.0

Details
========

    install and configure apache2, mysql5.0, scrapy, gallery2.0.  

    modify the directory name of image storage.  

    run the command 'scrapy crawl sina_image' in the crawl directory to start to crawl images.  

    you can set the number of crawling for one time and at the same time the url of images will be written into the database.  

    after crawling, execute the addimages.py to add the images into gallery2.  

    if all goes well, you can browse your images already.  

    of course, you can execute the above steps repeatedly to update your album.



