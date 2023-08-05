# Manipulating Colors

Once a `#!py3 Color` object is created, you have access to all the color channels. Color channels can be read
individually or extracted all at once. Getting and setting color channels is flexible and easy, allowing for intuitive
access.

## Reading Coordinates

There are various ways to read the current values of color coordinates.

1. Channel properties can be read directly by indexing the color object with the channel name.

    ```playground
    color = Color("orange")
    color['red']
    ```

4. The object can also be indexed with numerical numbers and even use slicing to set or get multiple values. Color
   objects can also be iterated.

    ```playground
    color = Color("orange")
    color[0]
    color[:-1]
    [c for c in color]
    ```

2. For more advanced get operations, the `get` method can be used. Channels can be accessed with normal strings:

    ```playground
    color = Color("orange")
    color.get("green")
    ```

    They can also be used to access values of the current color in terms of other color space properties. Simply
    specify the color space and the color property.

    ```playground
    color = Color("orange")
    color.get("lch.chroma")
    ```

## Modifying Coordinates

As with coordinate retrieval, a number of ways can be used set coordinates as well

1. Channel properties can be modified directly by using the channel. Here we modify `#!color red` by adjusting its
  `green` property and get an orange hued color.

    ```playground
    color = Color("red")
    color['green'] = 0.5
    color.to_string()
    ```

    When doing so, keep in mind that the internal coordinates are being adjusted, so their scale and range is dictated
    by the given color space in which they relate to. sRGB, for example, specifies its color channels in the range of
    \[0, 1\], though it should allow extended ranges if required.

2. Additionally, colors channels can be set with numerical indexes. Slicing can even be used to set multiple channels
   in one operation:

    ```playground
    c1 = Color('red')
    c2 = Color('blue')
    c1[:] = c2[:]
    c1, c2
    ```

3. More advanced set operations can be performed by using the `set` method.


    As these methods return a reference to the current class, multiple set operations can be chained together. Chaining
    multiple `set` operations together, we can transform `#!color white` to `#!color rgb(0 127.5 255)`.

    ```playground
    Color("white").set("red", 0).set("green", 0.5)
    ```

    Functions can also be used to modify a channel property. This allows us to do more complex set operations, like
    providing easing functions. Here we do a relative adjustment of the green channel and transform the color
    `#!color pink` to `#!color rgb(255 249.6 203)`.

    ```playground
    Color("pink").set('green', lambda g: g * 1.3)
    ```

    And just like the `get` method, we can use this method to set color channels in other color spaces.

    ```playground
    c = Color("red")
    c
    c.set('hsl.hue', lambda x: x + 180)
    ```

    ??? note "Notes on Modifying Coordinates in Other Spaces"

        As previously mentioned, coordinates in other spaces can be modified with the `set` function. Here we alter the
        color `#!color blue` by editing the `hue` channel in the CIELCh color space and get
        `#!color Color("blue").set('lch.hue', 130)`. Keep in mind that the colors are being converted to the specified
        space under the hood, set, and then converted back, so if you have multiple operations to apply in a given color
        space, it may be more efficient to convert to that space, apply the set operations directly, and then convert
        back.

        ```playground
        Color("blue").set('lch.hue', 130)
        ```

        When setting a color in another color space, the final value is subject to any rounding errors that may occur in
        the round trip to and from the specified color space. Also, depending on the transform functions of the spaces
        involved, and whether the original color is on the edge of its own gamut, this can lead to a color going
        slightly out of gamut, and if one of the spaces involved in the conversion doesn't handle out of gamut colors
        with sensible values, you may get something unexpected back.

        Consider the following example comparing the modification of an HSL color in HWB vs Oklab.

        ```playground
        Color('hsl(0 0% 50%)').set('hwb.blackness', 0).set('hwb.whiteness', 100)
        Color('hsl(0 0% 50%)').set('oklab.lightness', 1)
        Color('hsl(0 0% 50%)').set('oklab.lightness', 1).convert('srgb')[:]
        ```

        The above example cleanly converts between HSL and HWB as the conversion between these two is much more precise,
        but the Oklab example is not quite as precise and returns a color with a saturation that is way out of bounds.
        This is partly because the Oklab max whiteness isn't exactly `1`, but more like `~0.999...`, The HSL model
        doesn't really represent out of gamut colors in a logical way and, in this case, creates a color with a negative
        saturation. It looks worse than it really is as when we convert it to sRGB, we see it is barely off. None of
        this is a bug, it is just the nature of the algorithms we are using to convert, the precision of the floats, and
        the slight rounding errors that occur when using [floating-point arithmetic][floating-point], etc.

## Undefined Values

Colors in general can sometimes have undefined channels. This can actually happen in a number of ways.

1. Channels can naturally be undefined under certain situations as defined by the color space. For instance, spaces
with hues will have powerless hues when the color is achromatic. This can occur if saturation or chroma is zero, or
when a color has no lightness, etc.

    If a hue is manually defined to an achromatic color hue is considered defined, though that value will still be
    powerless during conversion. But lets considered an achromatic color in a rectangular color space being converted to
    a cylindrical color space with hue. During the conversion process, there is nothing to suggest to the algorithm what
    the hue should be. For instance, if saturation is zero, one could argue the hue should be `0`, but that is actually
    a red hue, and achromatic colors have no hue. In the end, no hue is actually satisfactory, so an undefined hue is
    applied.

    ```playground
    color = Color('white').convert('hsl')
    color[:]
    ```

2. When specifying raw data, and an insufficient amount of channel data is provided, the missing channels will be
assumed as undefined, the exception is that `alpha` channel which is assumed to be `1` unless explicitly defined or
explicitly set as undefined.

    ```playground
    Color('srgb', [1])[:]
    Color('srgb', [1, 0, 0], NaN)[:]
    ```

3. Undefined values can also occur when a user specifies a channel with the `none` keyword in CSS syntax. This can also
be done in raw color data by directly passing `#!py3 float('nan')` -- the provided `NaN` constant is essentially an
alias for this.

    One may question why such a thing would ever be desired, but this can be quite useful when interpolating as
    undefined channels will not be interpolated. It can be thought of as a way to mask off channels. Checkout the
    [Interpolation](./interpolation.md) section in the documentation to learn more.


    ```playground
    from coloraide import NaN
    color = Color("srgb", [0.3, NaN, 0.4])
    color[:]

    color = Color('rgb(30% none 40%)')
    color[:]
    ```

4. Lastly, a user can use the `mask` method which is a quick way to set one or multiple channels as undefined.
Additionally, it returns a clone leaving the original untouched by default.

    ```playground
    Color('white')[:]
    Color('white').mask(['red', 'green'])[:]
    ```

    The `alpha` channel can also be masked:

    ```playground
    Color('white').mask('alpha')[-1]
    ```

    You can also do inverse masks, or masks that apply to every channel not specified.

    ```playground
    c = Color('white').mask('blue', invert=True)
    c[:]
    ```

## Checking for Undefined Values

As previously mentioned, a color channel can be undefined for a number of reasons. And in cases such as interpolation,
undefined values can even be useful. On the other hand, sometimes an undefined value may need to be handled special.

Undefined values are represented as the float value `NaN`. And since `NaN` values are not numbers -- hence the name "not
a number" -- they don't quite work the same as normal numbers. They don't contribute to math operations like add,
multiply, and divide. Any math operation performed with a `NaN` will simply yield `NaN`. `NaN` values are essentially
infectious.

At first glance, the behavior of `NaN` values can seem confusing, but it is actually pretty intuitive. If we define a
color with an undefined channel, and try to add to that value, what should we get? In reality, if the value is
undefined, how could we possibly add to it? The only sane answer is to return `NaN` again.

```playground
color = Color('color(srgb 1 none 1)')
color['green'] + 0.5
```

Because a `NaN` may cause surprising results, it can be useful to check if a hue (or any channel) is `NaN` before
applying certain operations where `NaN` may be undesirable, especially if the color potentially came from an unknown
source.To make checking for `NaN`s easy, the convenience function `is_nan` has been made available. You can simply give
`is_nan` the property you wish to check, and it will return either return `#!py3 True` or `#!py3 False`.

```playground
Color('hsl(none 0% 100%)').is_nan('hue')
```

This is equivalent to using the `math` library and comparing the value directly:

```playground
import math
math.isnan(Color('hsl(none 0% 100%)')['hue'])
```
