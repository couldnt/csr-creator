# CSR Creator (csr-creator)

**CSR Creator** is a convenient tool which can help you to create the **Private Key** and **CSR** ([Certificate Signing Request](https://en.wikipedia.org/wiki/Certificate_signing_request)) for **SSL certificate**.

It is a web application written in **Python** based on [Flask](http://flask.pocoo.org/), [plumbum](https://plumbum.readthedocs.org/) and [Bootstrap](http://getbootstrap.com/).


## Why?

In my daily work, I always need to create the CSRs for different domains for my customers, usually I log into a linux server, then use openssl command to create the Private Key and CSR files, then download (SCP) them from the server and send to my customer.

Even I am a software engineer and know linux well, I still think this process is not convenient, so a web-based application would be the best way to provide the convenience.

## Installation
To run the CSR Creator, you need to install Flask and plumbum first.

* Install Flask, run pip install Flask
* Install plumbum, run pip install plumbum

Then, run python csr.py, you will see
> Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
>
> Restarting with stat
>
> Debugger is active!
>
> Debugger pin code: 336-049-928

Then open you browser, and visit [http://127.0.0.1:5000/csr](http://127.0.0.1:5000/csr).

## Screenshots

![](http://i.imgur.com/l2PlHVg.png)

![](http://i.imgur.com/jC3b5Dq.png)