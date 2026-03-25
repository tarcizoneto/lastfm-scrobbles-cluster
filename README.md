
# last.fm Scrobble Cluster
A tool to ***clean*** ~~(kind of)~~ your **last.fm history** by **merging duplicate tracks' scrobbles**. It re-scrobble tracks that were **mistakenly scrobbled** under a **different URL** with a lower playcount, consolidating them into the URL with the **highest playcount**.

In short, [lastfm-scrobbles-cluster](https://github.com/tarcizoneto/lastfm-scrobbles-cluster) can be used when the **same track** appears in **multiple scrobble pages**, but it should exist as a **single page**, this script **merges** their scrobbles together.


## Applications
*When I switched from Spotify to Apple Music, some of the tracks that I were listened were being scrobbled in a new page, and not in the already existent, so it created two different clusters, and the highest playcount page wasn't being used.*
> Most commom causes of duplicate tracks between Apple Music and Spotify:
>> Tags delimitation
> * In *Apple Music*, the majority of **song tags** are delimited by **(** *tags* **)**, as in this tracks' page: 
>  ![Apple Music tag delimitation; picture of a track scrobble history in last.fm](assets/tracktags2.png)
>  
>  * And in Spotify, the majority of **song tags** are delimited by  *songname* **-** *tags*, as in this tracks' page: 
>  ![Spotify tag delimitation; picture of a track scrobble history in last.fm](assets/tracktags1.png)
>  
- Even when there are **slight changes** in a track title, **last.fm** can **not** **detect** if there is already an **existent page** with older scrobbles in a **different title**, *it* takes the **easy way out** and creates new track pages at every minimum change of the title, **creating a bunch of scrobble clusters**.
>> Artists in a collaboration track
> - *Note on the artist names:*
> 
> *(Apple Music)*
> ![Apple Music artist scrobble assignment; picture of a track scrobble history in last.fm](assets/trackartist1.png)
>
> *(Spotify)*
>![Spotify artist scrobble assignment; picture of a track scrobble history in last.fm](assets/trackartist2.png)
- Perhaps, this is a problem in AM's official scrobbler, instead of **scrobbling on the page of the main artist**, the scrobbles appears in a **new page**, with the exact same track name, but with all the **artists merged with "&"**

Note that, *not only at these causes*, [lastfm-scrobbles-cluster](https://github.com/tarcizoneto/lastfm-scrobbles-cluster) can detect almost any type of duplicate tracks by: **detecting** their **title tags** and **comparing** titles and tags with **possible lookalikes**; **detecting** exact **same tracks** in **different pages** and **detecting wrong artist assignment**.
After all that, it selecting the page that has the highest playcount and **re-scrobbling the improperly scrobbles.**

*I hate when these duplicate pages are created, and, as I am a *LOVER* of ranking tracks in last.fm, this tool is really useful for me by merging those.*

