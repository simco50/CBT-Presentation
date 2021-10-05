---
theme : "Blood"
transition: "none"
highlightTheme: "monokai"
slideNumber: true
title: "Concurrent Binary Tree"
autoPlayMedia: true
controls: true
progress: true
enableChalkboard: true
---

<!-- .slide: data-background-video="resources/CBT_Main.mp4" data-background-color="#000000" -->

### Adaptive Subdivion on the GPU

##### Concurrent Binary Tree & Longest Edge Bisection

note: Hello everyone. A couple months ago, I attended virtual SIGGRAPH and while there was a ton of interesting content and talks, there was one in particular that really got my attention which was a presentation by some graphics engineers at Unity who have implemented terrain rendering with adaptive subdivion inside Unity with this novel data structure called a Concurrent Binary Tree.
After seeing the presentation and later reading the paper, I decided to try and implement this myself based on the paper and what you see here in the background is the result of my implementation, though as you can see no artistic touch whatsoever :).
So based on those results and findings, I'd like to talk about adaptive subdivision on the GPU using concurrent binary trees and longest edge bisection.
The title is quite a mouthful of words, but I wouldn't worry, because it's actually not as complicated as it sounds and I hope that when I finish talking you'll understand how it works.

---

### Manim

[_video source_](https://www.youtube.com/watch?v=ocVSfWo3MLY)

<video src="Resources/BubbleSortDemo.mp4">

note: Before I jump in. I recently found out about this open source Python library called Manim. It's the library used to make math instructional videos created by Grant Sanderson or his more familiar sounding Youtube channel called 3Blue1Brown.
I decided to play around with it and I ended up implementing a part of the subdivision algorithms in Python to be able to visualize it.
I think this library is super cool and the video you see here is just an example I took from YouTube to show you what it can do.
I hope some of the videos throughout the slides will help you better understand the algortihms.

---

## Skip to the results

note: So let's jump into it. Like I said, the title of this presentation is quite the mouthful so I'd like to start with a little demo first to give you an idea of what exactly we try to achieve here.

---

### Loads of material!

#### [Jonathan Dupuy]((https://onrendering.com/))

![](Resources/PaperCover.png)

note: All of this work is almost entirely based on the work of Jonathan Dupuy, who's a research engineer at Unity. If you want to learn more about this tech, I highly recommend checking out his initial presentation about it on YouTube

---

### Adaptive Subdivision

Tessellation shaders, Geometry shaders?

Subdivision = Recursive Algorithm = Exponential Cost

- Adaptive: Subdivide where necessary
- Parallel: Multithreaded, on GPU

note: Subdivision is a pretty well researched topic in computer graphics and ranges a huge amount of techniques going from very simple to pretty complicated stuff. 
It is a recursive algorithm which fundamentally makes it exponential in computation cost.
There's a few available options around there like the Tessellation Shader but for those who are familiar with it, it doesn't have good performance, doesn't produce good topology and still isn't well supported on certain platforms.
Essentially what we want is to be able to amortize the exponential cost by subdividing adaptively, in parallel and over several frames.

---

### Subdivision as Binary Trees

Leaf nodes describe triangles via the path they form from the root

<video src="Resources/renders/hq/UniformLEB_WithTree_Main.mp4">

note: This brings me to the idea proposed in the paper. The canonical subdivision can be represented with a binary tree with each level of the tree representing a subdivision level. Think about it as the root node of the tree being a single large triangle and then splitting the triangle is done by splitting the node into two children. The leaf nodes of the tree then represent the triangles.
This means, if we find a way to parallelize operating on the nodes of a binary tree, we can accelerate our subdivision.
In other words, what we want, is to be able to process each leaf node in the binary tree indepedently on the GPU by either spliting it or merging it without data access conflicts or race conditions.

---

#### Longest Edge Bisection (LEB)

note: I'd like to split the problem in two parts: Rendering the triangles represented in the binary tree, and update the binary tree efficiently based on a ruleset with that ruleset basically resulting in adding more detail the closer the camera is to the triangle. I'm going to start by describing the approach to render the triangles first. For this we use an algorithm called Longest Edge Bisection.

---

Uniform Subdivision

<video src="Resources/renders/hq/UniformLEB_NoTree_Main.mp4">

note: Longest Edge Bisection (or LEB for short) is a fancy name for possibly the simplest subdivision scheme in existance. You take a triangle and you split it in half along it's longest edge leaving you with 2 triangles. And this can be done recursively to achieve more subdivision.
This fits exactly with the binary tree idea.
For uniform subdivision, each subdivision, the amount of triangles will double due to its exponential nature.
As you can see in the video, we assign each triangle a value starting from 1 which match the binary tree indices starting from the root node of the tree.

---

Binary

<video src="Resources/renders/hq/UniformLEB_Binary_Main.mp4">

note: Now let's look at this again but show each triangle value's in it's binary representation.
There's two interesting things we see here. The subdivision depth of each triangle is defined by the number of bits of the triangle index. 
And the least significant bit - or rightmost bit - defines if the triangle gets split to the left side or the right side.

---

LEB Split Matrix

<video src="Resources/renders/hq/LEBMatrices_Main.mp4">

note: 
With these two observations in mind, the subdivision algorithm can be implemented per triangle by scanning over all the bits in the index of the triangle and recursively multiplying a so called split matrix based on if that bit is a 0 or a 1.
The left matrix above scales and shifts the triangle vertices to the left side, and the right matrix does the same but for the right side.
It doesn't take long to realize both are almost identical and we can just plug in a parameter based on the bit value.
So almost the entire algorithm is done with this single matrix.

---

Pseudo

```c++
depth = firstbithigh(nodeIndex);
bitID = depth - 1;
matrix = IdentityMatrix()
for(bitID = depth - 1; bitID >= 0; --bitID)
{
    splitMatrix = GetSplitMatrix(GetBitValue(nodeIndex, bitID));
    matrix = mul(splitMatrix, matrix);
}
triangleVertices = mul(matrix, baseTriangle);
```

note: So the algorithm boils down to a for loop over all the bits of the node index and sequentially multiplying the appropriate split matrix.
I can understand all of this may still sound a bit abstract but I think a concrete example will make it clear how it works and make you realize how simple this actually is.

---

<video src="Resources/renders/hq/LEBBitScan_Demo1.mp4">

note: So let's say we want the vertices of the triangle with value 39. This has the binary representation 100111. We start with an identity matrix. We scan the binary value starting from the most significant bit, grab the appropriate split matrix based on if it's a 0 or a 1, and multiply it with the previous matrix. Once that's done, you're left with a matrix you can multiply with the base triangle and those are the vertex positions of the triangle which are shown in the top right.

---

Another!

<video src="Resources/renders/hq/LEBBitScan_Demo2.mp4">

note: Here is another example, let's take triangle 52 to confirm this algorithm is independent of which triangle you pick.
Again, start with the base triangle and an identity matrix, scan each bit from MSB to LSB and multiply by the appropriate split matrix. Then multiply the base triangle with the composed matrix and that's it.

---

Adaptive Subdivision

<video src="Resources/renders/hq/AdaptiveLEB_NoTree_Main.mp4">

note: Now I think that's pretty elegant and it's not that hard to make this adaptive. Adaptive subdivision has essentially the same principles but we subdivide our triangle based on a target criteria, for example this point.
You recursively check if the target is inside the triangle and if it is, we split it.
Notice that the following video actually has a problem, partially due to me procrastinating to finish making this presentation and therefor having too little time but also to prove a point, which is that it creates so called T-juctions which are the vertices touching the middle of an edge and that will cause cracks in the geometry. Imagine there being a height offset at that point, there is no way for that larger triangle to match the deformation of its neighboring triangles and we want to avoid that.

---

<video width="650px" src="Resources/AdaptiveLEB.mp4">

note: So here with a video capture in application where this problem is solved. We do this by making sure a neighboring triangle is never more than 1 level different in subdivision. This can be implemented by adapting the splitting and merging operation. Whenever a triangle wants to be split we have to split the neighboring triangles recursively until the rule is satisfied and when a triangle wants to be merged, its longest edge neighbors also needs to be merged without breaking the rule as they need to be merged at the same time to avoid cracks.

---

### Binary Tree

<video src="Resources/renders/hq/AdaptiveLEB_WithTree_Main.mp4">

note: So going back to the idea from the start, because the LEB algorithm splits the triangle in two, it can be associated with our binary tree with the triangles being leaf nodes of the tree. Splitting a triangle in two then means splitting the node into two children.
So we now have the algorithm to be able to render the triangles described by a binary tree representing subdivision.

---

### "Concurrent" Binary Tree

<video src="Resources/renders/hq/BinaryTree_ExampleTree.mp4">

note: This is the main subject of the paper which is the novel data structure that allows updating of a binary tree in parallel.
Manipulating a regular binary tree data structure in parallel is not efficient so that's where Concurrent Binary Tree (or CBT) comes in.
In essence, a CBT looks like a binary tree but it actually encodes the actual binary tree.
It's formed of 2 parts: a bitfield with bits equal to the amount of maximum leaf nodes and a sum reduction tree which stores the sum of child node values from bottom to top.
The bitfield alone can actually represent the binary tree but the sum reduction tree will become a key part to be able to parallize the workloads. The bitfield is encoded using 32 bit integers because we can't directly modify individual bits directly in I think probably any programming language.

---

#### Encoding a binary tree with a bitfield

<video src="Resources/renders/hq/BitfieldToTree_Main.mp4">

note: The bitfield alone encodes the entire binary tree. The way that works is that each one in the bitfield represents a leaf node of the actual tree. 
Take for example the last bit here, to compute which node it's associated with, we simply count the number of zero's that come after it, add one and take the log2 of that. For this example, there's three zeros which means the result of that formula is 2 and so starting from the bottom, we go 2 layers up and reach index 3.
That means that for example a fully split binary tree is represented by a bitfield with all 1's and a binary tree with a single root node is just a single 1 followed by all 0's.

---

#### Splitting and merging

Split node 3 and merge node 4.

![](Resources/Example_SubDiv_01.png)

note: What makes this so powerful is that we can describe node splitting as setting the right child bit to 1 and node merging as setting the right child bit to 0. This can be done in parallel as long as these modifications are done with atomic operations like InterlockedOr and InterlockedAnd.
Take this tree for example.

---

#### Split

Set right child bit to 1

![](Resources/Example_SubDiv_Split.png)

note: To split for example node 3, we simply take the right child node, get its corresponding bit in the bitfield and set that to 1.
Also see how the left child index is always 2 times the node index of the parent and the right child index is that plus one. So this is super fast to compute.

---

#### Merge

Set right child bit to 0

![](Resources/Example_SubDiv_Merge.png)

note: Node merging is very similar. Take the right child node, and set its corresponding bit to 0.

---

### Sum Reduction Tree

Map ThreadID -> Leaf Node

node: So the bitfield encodes the binary tree and we can implement splitting and merging by setting the corresponding bit to either 1 or 0 respectively.
Now when we have a binary tree with let's say 12 leaf nodes, we have to dispatch a shader with 12 GPU threads to process each nodes.
We'll need an efficient way to associate each GPU thread with a leaf node.

---

![](Resources/BinarySearch_Example_01.png)

note: Say we're looking for the leaf node associated with thread number 2. As we've seen before, we can count the bits after the third one in the bitfield and compute the node index that way, but that's terribly inefficient because we'll have to scan the entire bitfield from the start. For a tree of depth 25 that's over 30 million bits.
The purpose of the sum reduction tree is to accelerate this. It's built by adding the value of each child pair and storing it in its parent from bottom to top. With this, you can do a binary search from top to bottom to find the node association much more efficiently.
So before each subdivision pass, the sum reduction tree has to be updated.

---

![](Resources/BinarySearch_Example_02.png)

note: So moving forward with this example, the binary search works as follows. We have our thread index 2 and start from the top of the tree.
We compare the thread index with the left child node's value and step to the left child as our thread index is smaller than that value.

---

![](Resources/BinarySearch_Example_03.png)

note: Now we do the same again.

---

![](Resources/BinarySearch_Example_04.png)

note: Compare the thread index with the left child. This time we step to the right child because our thread index is larger than the left child's value.

---

![](Resources/BinarySearch_Example_05.png)

note: When stepping to the right child, we subtract the left child's value from our thread index. If you keep doing that until the value is smaller than 1, the node you end up on is the node associated with the thread index.

---

#### High level Subdivision code

```
for(triangleIndex : triangles)
    nodeIndex = cbt.BinarySearch(triangleIndex);
    lod = ComputeLOD(GetTriangle(nodeIndex));
    if(lod > 1.0f)
        cbt.Split(nodeIndex);
    else
        mergeTop = ComputeLOD(GetTriangle(TopTriangle)).x < 1.0f;
        mergeBase = ComputeLOD(GetTriangle(BottomTriangle)).x < 1.0f;
        if(mergeTop && mergeBase)
            cbt.Merge(nodeIndex);
```

note: With knowing how to perform splitting and merging and mapping the thread index to each leaf node, the subdivision algorithm can be implemented as those are the main building blocks. Each GPU thread takes a triangle by doing the binary search I've described, computes the LOD value based on user defined criteria such as camera distance and frustum culling, and either splits or merges the triangle based on that LOD value. See here how when merging, like I've mentioned before, we have to make sure the longest edge neighbor wants to merge too to avoid cracks.

---

### CBT + LEB Update loop

<video src="Resources/renders/hq/UpdateFlow_Normal.mp4">

note: Zooming out a little, here are the high level stages or "render passes" that run per frame to perform the adaptive subdivision.
The indirect arguments are retrieved from the root node of the CBT which represent the amount of leaf nodes.
Then we can dispatch the exact amount of threads on the GPU to perform the subdivision. That's followed by the sum reduction pass and eventually we can use that data to render our triangles. 

---

### Mesh Shader loop

Subdivision + Rendering in a single shader!

Per triangle frustum culling and expansion.

<video src="Resources/renders/hq/UpdateFlow_MeshShader.mp4">

note: Not so long ago, GPU vendors have introduced so called mesh shaders. For the unfamiliar, these fancy new hipster shaders replace vertex shaders, geometry shaders and tessellation shaders including the fixed function input assembler. It allows you to implement it yourself using a compute shader-style interface. So instead of doing subdivision and rendering separately, you can implement the subdivision in an amplification shader and from within that shader, you can dispatch mesh shaders on the GPU to form triangles. Another advantage of mesh shaders is that they can produce extra triangles and remove triangles similar to geometry shaders without any of the downsides. This allows you to further subdivide each triangle from the CBT in even more triangles. In my implementation, I divide each triangle into 128 more triangles. The advantage of being able to remove triangles is that you can perform per triangle frustum culling to further reduce rendering cost. That is technically also possible with a geometry shader but I found that to be much less efficient being twice as costly.

---

### LOD Criteria

- Screen size
- Frustum culling
- Local displacement/curvature
- Retain silhouette for shadows 

note: The subdivision algorithm allows you to make LOD decisions for each individual triangle. This can be completely arbitrary but I imagine most of the time the criteria are these. The idea is to keep the size of each triangle equal in size on screen. Meaning triangles far away from the view will be subdivides less. We can also stop subdividing triangles outside the view, and not subdivide in areas where we don't need to. For the terrain example, we don't have to subdivide areas where it's completely flat.
We can compute these criteria per triangle on the GPU very efficiently and based on those metrics, you can decide if you want to split or merge the triangle.
Another interesting opportunity for research would be subdividing to retain just the silhouette when rendering shadow maps. Each view including shadows would need its own CBT so it can make its own subdivision decisions.

---

### Storage

Define max subdivision before hand.

<span>
\[\begin{aligned}
VRAM = 2^{D+2}\, bits
\end{aligned} \]
</span>

Grows exponentially

| Depth | Size | Leaf nodes (Triangles)
| --- | --- | --- |
| 24 | 8.0 MB | 8 388 608  |
| 25 | 16.0 MB | 16 777 216 |
| 26 | 32.0 MB | 33 554 432 |
| ... | ... | ... |

note: The required storage for a CBT depends on its max depth and grows exponentially for each extra level due to its recursive nature. A tree with 25 nodes for example needs exactly 16 MB of memory and would mean more than 16 million leaf nodes when fully split. 
The naive approach would be to store each node in an 32 bit integer but that would be extremely wasteful because for example the bitfield only needs a single bit per node. So more on that next.

---

## Packing Data

We know exactly how many bits each node needs!

| Depth | Bits/Node
| --- | --- |
| D | 1 bit |
| D - 1 | 2 bits |
| D - 2 | 3 bits |
| D - 3 | 4 bits |
| ... | ... |

note: An neat insight here, is the fact that we know exactly how many bits each node needs depending on its depth. The bottom level can only be either a 0 or a 1, so we only need 1 bit to represent that. The level above adds two 1 bit values together, so we only need 2 bit to represent that. The level above that adds 2 2 bit values together so we only need 3 bits for that. Doing this type of packing will exactly halve the memory cost of the tree.
However, we can't simply modify certain bits in a datastream as all data is encoded in an array of 32 bit integers. Therefor, you have to compute the bit and elements offsets yourself and do some bit operations to set the right bit range. Because several GPU threads can access the same integers, all access to this data needs to be atomic.

---

### What's next?

- Unity's future terrain rendering algorithm.
- Suitable for water rendering?
- More subdivision?
- UE5's Nanite

![](Resources/nanite.png)

note: So I think this technique is extremely promising and I've been surprised at how easy this all is to implement in practice be it either on the CPU or GPU. This algorithm will become Unity's future terrain rendering algorithm and I wouldn't be surprised if they're experimenting with applying this to water rendering as well.
However, there's still a desire to reach more subdivision without the great exponential memory and performance cost which I think will be very hard to solve. There are a few really clever tricks found to greatly optimize certain parts of this technique but there's still a lot of work to be done.
Any time I read something about subdivision schemes for games, I'm reminded by someone else always asking about how it compares and relates to Unreal Engine 5's Nanite. I think the goal is the same being per pixel triangle detail for which it's visually imperceptive to see LOD pops due to its subpixel property. I think Nanite however has solved the several major road blocks to achieve this while nobody came close before. Per pixel triangles are prohibilively expensive on today's GPU's due to its design and I think the CBT subdivision scheme won't get close to Nanite without the software rasterization and compression that it has. However, Nanite doesn't support any form of runtime tessellation or displacement yet so in reality it can't achieve this today.

---

- [Advanced in Realtime Rendering 2021](http://advances.realtimerendering.com/)
- Dupuy 2020 ["Concurrent Binary Trees (with application to longest edge bisection)"](https://onrendering.com/data/papers/cbt/ConcurrentBinaryTrees.pdf)
- Dupuy 2021 ["Concurrent Binary Trees (paper presentation)"](https://www.youtube.com/watch?v=Wr3yIJ927EE)
- Deliot and Yao 2021 ["Experimenting with Concurrent Binary Trees for Large Scale Terrain Rendering"](http://advances.realtimerendering.com/s2021/Siggraph21%20Terrain%20Tessellation.pdf)
- Dupuy [Longest Edge Bisection demo on Github](https://github.com/jdupuy/LongestEdgeBisection2D)
- [Manim Community](https://docs.manim.community/en/stable/index.html)

note: These are my references for my work

---

#### Source code and slides on GitHub

**Source**: github.com/simco50/D3D12_Research/tree/CBT

**Presentation**: simco50.github.io/CBT-Presentation/index#/

note: And the source code for my implementation is on GitHub and so is this presentation in case you're curious in checking it out.