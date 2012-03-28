# -*- coding: utf-8 -*-
import application
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app = application.app
        app.config['TESTING'] = True
        self.app = app.test_client()
        application.drop_db()
        application.create_db()

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Sorry no projects for you today' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.app.post('/register', data=dict(
            username=username,
            password=password,
            confirm=password,
            email='weaea@dsa.com',
            image='john hawk'
        ), follow_redirects=True)

    def adding(self, title, description):
        return self.app.post('/add', data=dict(
            title=title,
            description=description,
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
            image_link='http://s3.amazonaws.com/ksr/projects/76336/photo-full.jpg?1329244834'
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('jonny', 'qwe123')
        assert 'Sorry no such user' in rv.data
        #rv = self.logout()
        #assert 'You were logged out' in rv.data

    def test_reg(self):
        rv = self.register('jonny','qwe123')
        assert 'Thanks for registering' in rv.data

    def test_login_again(self):
        rv = self.login('jonny', 'qwe123')
        assert 'jonny' in rv.data

    def test_adding_thanks(self):
        rv = self.adding('one','This is testion for test purposes')
        print str(rv)
        f = open('test.html' , 'w')
        f.write(str(rv.data))
        f.close
        assert 'Previous' in rv.data


if __name__ == '__main__':
    unittest.main()

