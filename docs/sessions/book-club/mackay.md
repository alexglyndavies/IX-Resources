# Book Club - Short Course on Information Theory

Please add in your questions / things you would like to discuss for the upcoming book club sessions.

## Week 1 (19th May 2026) - Chapter 1: Introduction to Information Theory

- Discussed the format of the book club - shared document for adding questions.
- "There are no unknown perfect codes over finite fields" [Tietavainen, *SIAM J. Appl. Math.*, Vol. 40, No. 1, Jan. 1973].

## Week 2 (26th May 2026) - Chapter 2: Probability, Entropy and Inference

- Remind me of Integrated Information Theory (IIT) as a topic which could be interesting for the cohort as an attempt to provide a quantitative description of consciousness which then has application to philosophy of AI. An interesting point for me is: "different physical systems with different internal causal structure may perform the same input-output functions."
- "One of the themes of this book is that data compression and data modelling are one and the same, and that they should both be addressed ... using inverse probability."
- Proof of Gibbs' inequality shows that the result is true if you replace $-\log$ with any other convex function, and it turns out there is an appropriate zoo of such things: [f-divergences](https://en.wikipedia.org/wiki/Divergence_(statistics)#f-divergences).

## Week 3 (2nd June 2026) - Chapter 4: The Source Coding Theorem

- "The Shannon information content makes sense: it measures the length of a binary file that encodes x."
- The "optimum strategy is one that maximises expected information (i.e. entropy) at each choice" is one I have seen applied to Wordle. This is perhaps not important but a bit of fun in a game that does not feel arbitrary.
- It might be an interesting thought exercise to consider the information required for an (L)LM to work. Predicting the next token with no context is very hard, but context gives information. For example, consider a simple model where tokens are letters and one is predicting the next letter in a name, as in the Wenglish example. $(1/26)^5$ is low compared to $1/32786$, and after two tokens one may have an even better chance of predicting. How should we formalise this intuition?
- I found the proof of the source coding theorem very unintuitive. Does anyone have insight here?
- <https://scienceline.org/2006/07/tech-schrock-20q/>

## Week 4 (9th June 2026) - Chapter 5: Symbol Codes

- Imagine solving the optimal symbol code problem using Lagrange multipliers, that is minimise $\sum p_i l_i$ such that $\sum 2^{-l_i} = 1$. This works without dealing with discrete code lengths. Should we be concerned? The proof of Theorem 5.1 just takes the ceiling, but comments that these may not give optimal.
- The Kraft inequality for binary codes can presumably be generalised to the condition $\sum n^{-l_i} \leq 1$ for alphabets of size $n$ by considering that you can encode an alphabet of size $n$ with binary codewords of length $\log_2(n)$.
- How do we prove that bisecting subsets gives rise to $L(C, X) \leq H(X) + 2$? I cannot get this.
- <https://cstheory.stackexchange.com/questions/8314/comparing-shannon-fano-and-shannon-coding>

## Week 5 (16th June 2026) - Chapter 6: Stream Codes

- Exercise 6.1 provides the answer to the bisecting subset question.
- The "big picture" makes the point clearly - exponential improvements in encoding cost for a given fixed-length sequence, but also flexibility as the input stream comes in.
- Laplace's rule and other methods of "additive smoothing" using pseudocounts is on my mind at the moment in terms of answering the question: "what model of smoothing should be used?"
- The comment on efficient data-entry devices makes me think of an old idea: navigating Google Maps is similar to finding geodesics in hyperbolic space. To go from one place to another we zoom out from the start until both points are visible, then zoom in on the second. Presumably an efficient way of encoding important points on the map is given by how much one needs to zoom in on them to fix them directly.
- The discussion about where LZ compression fails is very enlightening, with the comment about the use of AI being relevant for this cohort. In the simple case of Fig. 6.11, just "transposing" the image would greatly improve compression. Perhaps we view this as an example of where one learns a representation of data where existing high-performance coding algorithms achieve their best rates.
- Playing around with this LZ compression can lead one to think of fun ways to waste time, e.g. how would it compress <https://oeis.org/A008836> and how does this relate to the Riemann hypothesis?
