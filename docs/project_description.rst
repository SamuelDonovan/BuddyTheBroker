.. toctree::
   :maxdepth: 2
   :caption: Contents:

Project Description
===================

General Overview
----------------

A raspberry pi 4 will be positioned upon Buddy's feeder equipped with a screen and a camera
(all he will need to make his stock selections). The screen attached to the raspberry pi 4 will cycle
through potential stocks, displaying a new stock ticker at a consistent interval. When a stock ticker is
displayed that Buddy finds to be a sound investment he will sit in view of the attached camera for at
least half of the interval in which that stock ticker is displayed on the screen. The raspberry pi will
determine whether or not Buddy is sitting in front of the camera using computer vision. If the camera
has recognized Buddy as in view for half of the trading interval that the stock ticker is displayed then
the system will make note his stock selection and open a buy order. Once his account depletes its
purchasing power and he no longer has enough funds to execute his next stock pick the first stock he
purchased will be sold to allow for him to continue making purchases. This first in first out nature will
continue as he makes more and more stock picks. To not get Buddy's account flagged as a pattern day
trader he will be limited in the amount of buys that he can execute each day.

How does buddy know where to stand? Buddy’s feeder is set up on timer giving him constant
meals each day. Due to this consistency each day he lines up in font of his food dish a fair bit of time
before his food will be dispensed. Some meals he is front and center of his food bowl well over an hour
before its time for him to be feed. Other meals he may only show up five minutes before hand. Some
times he will stand in front of his bowl just hoping that it is feeding time and give up after a while. This
inconstant behavior can be leveraged as mechanism for his stock picks.

.. figure:: images/project_description/ov1_diagram.png
    :alt: OV-1 Diagram
    :align: center

    Figure 1: OV-1 Diagram With Call Out Boxes


The operation view one (OV-1) diagram, Figure 1: OV-1 Diagram With Call Out Boxes,
illustrates all of major components of the system. It can be seen that the system is broken into two
separate physical pieces.

The first physical piece of the system will contain the main computer which will be interfacing
with the camera and display. The camera will detect Buddy using computer vision. The display will be
used to display the ticker that is currently available for purchase. As described previously Buddy will
be drawn to the system due to its placement above his food dispenser.
The second physical piece of the system will contain another raspberry pi used for video
storage. This raspberry pi will be connected to a hard drive in a remote location, able to communicate
with the first raspberry pi over the local area network (LAN) using each raspberry pi’s WiFi
capabilities.

At this point it should be noted that several diagrams have been chosen to use the Department
of Defense Architecture Framework (DoDAF) methodology due to its ability to easily convey
intricacies of a system.1 Several operations views have been omitted, due to the relative simplicity of
the system those generated are sufficient in properly explaining the system.

Similar Work
------------

Before anyone goes doubting Buddy’s trading prowess and thinks an embedded project in
which money is burn via a remote control flamethrower would yield the same results it is worth noting
that this is not the first project of its kind and there is a level of scholarly thought on this subject. In
1973, Princeton University professor Burton Malkiel claimed in his book ‘A Random Walk Down Wall
Street’ that, “A blindfolded monkey throwing darts at a newspaper's financial pages could select a
portfolio that would do just as well as one carefully selected by experts.” 2 As it would turn out
Malkiel was wrong and monkey often do a much better job than the experts. 2 The Wall Street Journal
has replicated this experiment each year by choosing 100 random stocks from the S&P 500 and
interestingly enough it will often bet the S&P 500. 3 Even the man arguably most famous for investing
has given credence to this idea. Warren Buffett is quoted as saying, “A patient and sensible monkey,
who builds a portfolio by throwing 50 darts at a board that includes the entire S&P 500 Composite
Index could increase his capital.” 4

At this point it is worth pointing out that a monkey throwing darts is really a tongue and cheek
analogy for picking stocks at random. Some YouTube personalities have taken this more literally.
Graham Stephen in his video, “I Spent $100,000 On A Stock Picking Monkey”, allowed for an actual
monkey to chose ten stocks which would comprise a $100,000 account. 5 Several months later in his
video titled, “How To Make Easy Money In The Stock Market”, Mr. Stephen goes on to show that his
monkey account did in fact perform better than comparative indexes. 6 It is worth noting that others
have conducted similar experiments as well with one YouTube personality allowing for his fish to trade
stocks, which again outperformed the market. A link to said YouTube personality will not be provided
due to the inappropriate humor in said video.

The point to be made is that this is by no means a new idea nor is it one I would expect to fail
miserably. The goal of this project is to simply put a new spin on the idea and perhaps get my cat a new
scratching tower in the process.

Capabilities And Limitations
----------------------------

Capabilites
~~~~~~~~~~~

Capabilities will be covered at various levels of detail throughout this document. The main
sections to point out would be the following:

* Libcamera
* Libdisplay
* Libstock
* Libtrading
* Remote Storage (Open Media Vault Use Case)

Essentially the main capabilities will include a camera application programming interface (API)
with the ability to detect cats, a display API with the ability to display stock tickers, a stock API with
the ability to fetch various stock information, a trading API with the ability to buy/sell stocks, and the
ability to store video on a separate remote drive. These separate capabilities when combine make up the
indented use case for this project.

Limitations
~~~~~~~~~~~

Given the specificity of the goal of this project the design should enable it the end product to
achieve its desired goal without too many draw backs. The main two that I see with the current design
are:

1. Lack of processing power on the Raspberry Pi 4

While the Raspberry Pi 4 is an impressive little computer, computer vision is no easy task. For
this reason the frame rate or even quality may be severally limited. Since the use case of this design is
to only ensure that a cat is present for several minutes at a time this should be a trade off that is easy to
live with. If this project needed to detect a multitude of different objects with millisecond precision this
would be an issue, but for the purpose of this project a Raspberry Pi 4 should be more than enough.

2. Using a static list of stocks

The current planned implementation uses a pre-downloaded list of stocks to form the data frame
used for stock data. The current list of stocks includes the top 1000 U.S. stocks sorted by market
capitalization. Should this order change in the near future the order in which the stocks are presented
could be slightly unaligned with the current market. Or if stock number 1000 is having a bad month
and stock number 1001 is having a good month the placements could swap leaving my system with a 
stale data set. For the purpose of this project the easy of using a pre-downloaded data set outweigh
these drawbacks. The order in which the stocks are presented is not incredibly important so long as
they are presented in an even distribution giving each a likely chance to be bought. Similarly, if stock
number 1001 is bought over stock number 1000 it doesn’t seem it would terribly effect the overall
functioning of this project given that these stocks will likely be bought and sold relatively frequently.