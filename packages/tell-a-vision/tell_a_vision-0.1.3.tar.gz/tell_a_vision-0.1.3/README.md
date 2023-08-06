# tell a vision 📺
"https://github.com/rezmansouri/tell_a_vision/blob/main/misc/import.gif"
<p align="center">
  <img src="misc/import.gif" width="400em"/>
</p>

## Introduction
Usually, object detection projects present their output in a visual format that shows the objects found with bounding boxes in different colors representing their classes. Something like this:

<p align="center">
  <img src="misc/dog-bike-truck.png" width="400em"/>
</p>

But what if we could make the computer tell us what it is seeing? For example: "There is a dog in the bottom left, a bicycle in the middle, and a truck on the top right." What if the computer can *tell a vision*? Pretty cool right?

**tell a vision (`tv`)** is Python package that can provide explanatory analysis on the output of object detection algoirthms. It takes bounding boxes, and the classes of the objects found and answers questions such as:

- How many objects and of what kind are in a specific region of the scene?
- How far are they? Are they close? 
- Are they small or medium-sized?
- ...

And in the end, using TTS (Text To Speech) it can describe the scene.

Here is a mere representaion of what **`tv`** does:

<p align="center">
  <img src="misc/tv.gif" width="700em"/>
</p>