# -*- coding: utf-8 -*-
import application
import unittest
import random

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app = application.app
        app.config['TESTING'] = True
        self.app = app.test_client()
        application.drop_db()
        application.create_db()

    def tearDown(self):
        pass



    def login(self, username, password):
        return self.app.post('/login', data=dict(
            user =username,
            passw=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.app.post('/register', data=dict(
            username=username,
            password=password,
            confirm=password,
            email='weaea%s@dsa.com' % random.random(),
            image='https://secure.gravatar.com/avatar/b888d0bbe52d3a08505e62a60ff5cfc8?s=140&d=https://a248.e.akamai.net/assets.github.com%2Fimages%2Fgravatars%2Fgravatar-140.png'
        ), follow_redirects=True)

    def adding(self, title, description):
        return self.app.post('/add', data=dict(
            title=title,
            description="""What is the LowLine?We want to transform an abandoned trolley terminal on the Lower East Side of Manhattan into the world’s first underground park.  It will be a new kind of public space, using solar technology for natural illumination, and cutting edge design to capture and highlight a very special industrial space.""",
            httext = """hello
What is the LowLine?We want to transform an abandoned trolley terminal on the Lower East Side of Manhattan into the world’s first underground park.  It will be a new kind of public space, using solar technology for natural illumination, and cutting edge design to capture and highlight a very special industrial space.

A park… underground?!?Ever wonder why there's so little green space in New York?  There aren’t a lot of empty plots of land just waiting to be turned into new parks. New Yorkers have had to be a little more creative, and must look in unusual places – the High Line, a park built on an old elevated rail trestle, is a great example.

A few years ago, we learned about a massive unused former trolley terminal in our neighborhood, the Lower East Side. We got to thinking: what if we could build a park-- underground-- even if the space lacked natural sunlight?  So we explored using fiber optic cables to transfer sunlight below ground-- to support the growth of plants and trees.  As we shared this idea with others, people got excited.  "An underground High Line for the Lower East Side," they'd say.  "Kind of like... a LowLine."  The nickname stuck.

What is the space like?This "Delancey Underground" space is quite large, by New York standards: 60,000 square feet, or 1.5 acres -- nearly the size of Gramercy Park.  It was built in 1903 as a trolley terminal, for streetcars traveling over the Williamsburg Bridge, and has been out of operation since 1948.  We fell in love with the site because of its architectural details: old cobblestones, crisscrossing rail tracks, vaulted 20-foot ceilings, and strong steel columns.

Here's what's even more exciting: it's in the heart of the Lower East Side.  Our neighborhood is one of the oldest in the U.S., and has been home to generations of immigrants for centuries.  It is a center of diversity, culture, creativity, and innovation.

Let the Sun Shine... UndergroundTo build this park, we're planning to use a cutting-edge version of existing technology-- which we've already built in prototype. The system uses a system of optics to gather sunlight, concentrate it, and reflect it below ground, where it is dispersed by a solar distributor dish embedded in the ceiling.  The light irrigated underground will carry the necessary wavelengths to support photosynthesis-- meaning we can grow plants, trees, and grasses underground. The cables block harmful UV rays that cause sunburn, so you can leave the SPF-45 at home. Sunglasses optional (for cool kids).

What kind of a park is underground?  An awesome one.

We think a year-round public space will be valuable for everyone.  Farmers markets and vendor stands can feature fresh produce and locally made goods, supporting local and sustainable businesses.  Art installations, concerts, and performances can help showcase the incredible creative spirit of the Lower East Side.  Youth programming and educational opportunities can offer rich experiences for kids and parents.  And a safe haven from the hectic feel of Delancey Street will serve as relief in a very car-centric corner of Manhattan.

When it's really cold, or pouring rain, how much fun is it to hang out in Central Park?  The High Line?  Not so much.  The LowLine can be the 21st century answer to traditional parks: instead of building up, let's build down!

What we've done so farWe first presented this idea to our local community board in September, and have been overwhelmed with public interest ever since. We got some great press, from CNN to the New York Times to the Huffington Post.

We’ve spoken with the MTA – the State-r

                     world """,
            image_link='http://s3.amazonaws.com/ksr/projects/76336/photo-full.jpg?1329244834',
            goal_end='10',
            date_end='2012-3-31',
            lat=55.74 + random.uniform(-0.1,0.1),
            lng=37.62 + random.uniform(-0.4,0.4),
            loc="location",
            cat='cat111, cat11211, ca321t111, ca31t111, cat312111, ca31t111, c31at111,    ',
            types='me'
        ), follow_redirects=True)

    def comment(self, proj, comm):
        return self.app.post('/projects/%s' %proj, data=dict(
            comment=comm
            ), follow_redirects=True)

    def message(self, proj, mess):
        return self.app.post('/projects/send/%s' %proj, data=dict(
            message=mess
            ), follow_redirects=True)

    def parts(self, proj):
        return  self.app.get('/projects/add/%s' %proj)

    def adding1(self, title, description):
        return self.app.post('/add', data=dict(
            title=title,
            description=description,
            httext = "",
            image_link='http://upload.wikimedia.org/wikipedia/ru/thumb/5/58/The_virgin_suicides_OST.jpg/220px-The_virgin_suicides_OST.jpg',
            goal_end='2',
            date_end='2012-3-30',
            lat=55.74 + random.uniform(-0.1,0.1),
            lng=37.62 + random.uniform(-0.4,0.4),
            cat='cat2, cat4, cat14, cat124, cat314, cat414, c5at4, cat434, cat5224, ca5252t4, c5252at4, ca35t4, cat5324, cat4, cat4, cat4',
            types='pa'
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


        self.register('nonny','qwe123')

    def test_2(self):
        rv = self.login('jonny', 'qwe123')
        assert 'Sorry! No such user' in rv.data
        rv = self.register('jonny','qwe123')
        assert 'Thanks for registering' in rv.data
        rv = self.login('jonny', 'qwe123')
        assert 'You were logged in' in rv.data
        for i in xrange(20):
            self.adding('one %s' %i,'This is testion for test purposes')
        for i in xrange(20):
            self.adding1('two %s' %i,'This is testion for test purposes')
        rv = self.app.get('/')
        assert 'This is testion for test purposes' in rv.data
        for i in xrange(5):
            self.comment(40,'hello')
        self.app.get('/projects/add/40')
        self.register('bonny','qwe123')
        self.app.get('/projects/add/40')
        self.register('monny','qwe123')
        self.app.get('/projects/add/40')
        self.register('konny','qwe123')
        self.app.get('/projects/add/40')
        self.register('nonny','qwe123')
        self.app.get('/projects/add/40')
        self.register('lonny','qwe123')
        self.app.get('/projects/add/40')
        for i in xrange(5):
            self.message(40,'hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello hello')
        #rv = self.logout()
        #assert 'You were logged out' in rv.data

    def test_1(self):
        rv = self.login('jonny', 'qwe123')
        assert 'Sorry! No such user' in rv.data
        pass



if __name__ == '__main__':
    unittest.main()

