# Animate-js
Easy triggers for css animations using JQuery. Set up your css animations without a sweat using data annotation tags on HTML.

## Installation
Install the package via npm
```
$ npm install animate-js
```
Or download and copy the files

## Usage
1. If you do not have animations set up, you can install the awesome [animate.css](https://github.com/daneden/animate.css) package by daneden. Visit the site for more information on installation and usage.
2. Reference jQuery and your css file (or the Animate.css file) on your project head, then animate-js on your scripts section before the closing </body> tag.

    ```
    <head>
      <script src="js/jquery.min.js"></script>
      <link rel="stylesheet" href="lib/animate.css />
      ...
    </head>
    <body>
      ...
      <script src="js/animate-js.js"></script>
    </body>
    ```
3. Set the necessary data attributes for elements that need animating. Basic usage: 

    ```
    <div data-animation-condition="seen">
        <div data-animation="bounce infinite">
            <span>BOING</span>
        </div>
    </div>
    ```

##Now what?

Launch your site and make sure conditions are met to see the animation. With the example above, you need to scroll down and make sure at least half the parent element is visible. This should trigger the bounce animation on an infinite loop.

##Bare Minimum
At the very least, the parent element should have a 'data-animation-condition' attribute set up, and a 
```
<div data-animation-condition="seen">
    <p data-animation="fadeInRightBig">Swooosh</p>
</div>
```

##Data Attrributes

The following are the supported data annotations you can add to your HTML elements using __data-[attribute]__. Attributes marked with asterisks are required.

###Parent Element

<table>
  <thead>
    <td><strong>Attribute</strong></td>
    <td><strong>Default</strong></td>
    <td><strong>Description</strong></td>
  </thead>

  <tr>
    <td>*animation-condition</td>
    <td>-</td>
    <td>The condition that triggers the animation sequence of nested animatable elements</td>
  </tr>
</table>

###Nested Elements

<table>
    <thead>
        <tr>
            <td><strong>Attribute</strong></td>
            <td><strong>Default</strong></td>
            <td><strong>Description</strong></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>*animation</td>
            <td>-</td>
            <td>An array of comma separated animations. The animation plays for a specific element in the specified order.</td>
        </tr>
        <tr>
            <td>animation-timeouts</td>
            <td>[0]</td>
            <td>An array of comma separated timeouts in milliseconds.</td>
        </tr>
        <tr>
            <td>animation-infinite</td>
            <td>false</td>
            <td>Specifies if an element's animation sequence should be on a loop</td>
        </tr>
    </tbody>
</table>

##Animation Sequence and Timed Animations
The fun part is creating your own animation sequence. An element's animation is played in order, and if timeouts are specified, each animation waits that specified amount of time in milliseconds before playing the next.
```
    ...
    <div data-animation="fadeInRightBig, fadeOutLeftBig" data-animation-timeouts="100, 400" data-animation-infinite>
        <span>TO THE LEFT</span>
    </div>
    <div data-animation="fadeInLeftBig, fadeOutRightBig" data-animation-timeouts="350, 600" data-animation-infinite>
        <span>TO THE RIGHT</span>
    </div>
    ...
```

You can also set up intervals or delays before each element's animation. 
```
<div data-animation-interval="500" data-animation-condition="seen">
    <h2>Animating in Intervals</h2>
    <p>These animations play in intervals of half a second. </p>
    <p data-animation="fadeInRightBig">fade</p>
    <p data-animation="fadeInRightBig">in</p>
    <p data-animation="fadeInRightBig">from</p>
    <p data-animation="fadeInRightBig">right</p>
</div>

```

If you have noticed, the next animation starts as soon as the previous item starts playing, or if you haven't set up any delays or intervals, they all play simultaneously. Right now, the next animatable element within a parent element is triggered as soon as the current one starts playing. I will later on add an option for it to play before or after the Nth animation, but for now bear with what is available or you can fork this project. 

##Looping Animations (not for parent element)
There are two types of infinitely looped animations. The first example is having an **animation sequence** loop using the **data-animation-infinite** attribute.

```
    <div data-animation="fadeIn, pulse, fadeOut" data-animation-infinite>
        <span><3</span>
    </div>
```
In the above example, you should be able to see the heart appear slowly, pulse, then fade away repeatedly.

The other option is to setup the CSS animation to loop.

```
    <div data-animation="fadeIn, shake infinite, fadeOut">
        <span>BACON!</span>
    </div>
```
Notice that BACON shakes infinitely and doesn't fade out. This is because Animate-JS waits for the previous animation to end before attempting to play the next listed animation.

##Upcoming Features:
- Events to check when to reset animation group
- Animation loop on parent element
- An attribute for animation interval
- Manual triggers: $(elem).animate()
- More triggers: mouse hover & exit, voice comand, etc.
- Animation triggering without parent?
- Specify N amount of loop

##I was told there would be more functionality
__DON'T PANIC!__ I'm working on it! In the mean time, why not leave a comment or suggestion? I always appreciate constructive criticisms.
