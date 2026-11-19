<!-- 來源 S1
原始網址：https://www.nist.gov/cybersecurity/what-post-quantum-cryptography
實際網址：https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography
取得時間：2026-11-19T23:19:42+08:00
頁面標題：What Is Post-Quantum Cryptography? | NIST
轉換方式：scripts/fetch_web.py（只保留 <main> 內的標題、段落、清單） -->

**Official websites use .gov**


              A **.gov** website belongs to an official government organization in the United States.

**Secure .gov websites use HTTPS**


              A **lock** (  Lock
A locked padlock
) or **https://** means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

https://www.nist.gov/cybersecurity-and-privacy/what-post-quantum-cryptography

## [Cybersecurity and privacy](/cybersecurity-and-privacy)

# What Is Post-Quantum Cryptography?

IT experts can find technical resources on our [PQC standards page](https://csrc.nist.gov/projects/post-quantum-cryptography).

Additional information on transitioning to the new standards is available on our [NCCoE Migration to PQC page](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms).

*Researchers worldwide are racing to develop new devices called quantum computers, which could do many things conventional computers cannot — including breaking the defenses that secure confidential electronic information. NIST is leading a global effort to create electronic defenses against such attacks through its Post-Quantum Cryptography (PQC) project, which released*[*the first three finalized PQC standards*](/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)*in 2024. Read on for some answers to common questions about this developing technology and NIST’s efforts.*

## What are post-quantum encryption algorithms?

Encryption algorithms protect confidential electronic information, from email messages to medical records and financial statements, from unauthorized viewers. For decades, these algorithms have proved strong enough to defend against attacks using conventional computers that attempt to defeat the encryption. However, a new type of device under development called a quantum computer could break these algorithms, rendering our electronic secrets vulnerable to discovery.

To counter this looming threat, we need encryption methods that can stave off cyberattacks by both the conventional computers we know today and the quantum computers of tomorrow. These new methods are called post-quantum encryption algorithms.

## What is quantum computing?

A quantum computer draws upon different scientific concepts than a conventional computer does. It takes advantage of the quantum world’s counterintuitive properties — which enable a bit of data to act as both a 0 and 1 at the same time — to make calculations that would be difficult or impossible on a conventional computer.

If they can be built, sufficiently powerful quantum processors would be able to sift through many potential solutions to a problem simultaneously, zeroing in on the correct answer very quickly. This sort of sifting is a task that conventional computers cannot do very quickly or efficiently.

## Why are quantum computers being developed if they can potentially cause so much harm?

There are many helpful things quantum computers will likely be able to do.Quantum computers have the potential to accomplish tasks that involve the interplay of complex variables. These tasks include drug design, simulations of complex molecules, and solutions to the classic “traveling salesman” problem — finding the most efficient route through a number of destinations.

The quantum computing field remains in its infancy. Researchers must overcome major technical hurdles before they can build powerful quantum computers, and it is an open question as to how formidable quantum computers can become. However, advanced quantum computers remain a strong possibility, and they would have such a major impact on present-day encryption that the world must prepare for them.

## How does current cryptography work, and how would a quantum computer crack it?

Currently, many encryption algorithms rely on the difficulty conventional computers have with factoring large numbers. Sufficiently powerful quantum computers would not have this difficulty.

Conventional cryptographic algorithms select two very large prime numbers — which are only divisible by 1 and themselves — and multiply them to obtain an even larger number. While multiplying the prime numbers is easy and fast, it’s far more difficult and time-consuming to reverse the process and figure out which two prime numbers were multiplied together, and that’s what a conventional computer would have to do to break this encryption. These two numbers are known as the “prime factors.” For large enough numbers, a conventional computer has been estimated to need billions of years to figure out these prime factors.

A sufficiently capable quantum computer, though, would be able to sift through all of the potential prime factors simultaneously, rather than one by one, arriving at the answer exponentially more quickly. Experts have begun referring to such a mature device as a “cryptographically relevant” quantum computer.Instead of billions of years, it’s possible a quantum computer could solve this puzzle in days or even hours, putting everything from state secrets to bank account information at risk.

## Why do we need post-quantum encryption, and how will PQC algorithms work?

To stave off attacks by a quantum computer — if and when a cryptographically relevant one is built — the worldwide community must retire current encryption algorithms. Post-quantum encryption algorithms must be based on math problems that would be difficult for both conventional and quantum computers to solve.

The algorithms are designed for two main tasks for which encryption is typically used: general encryption, used to protect information such as passwords exchanged across a public network, and digital signatures, used for identity authentication.

Of the four algorithms NIST has selected as the initial ones to be standardized, three are based on a family of math problems called structured lattices, while the fourth uses mathematical relationships known as hash functions. Instead of requiring a computer to factor large numbers, lattice and hash problemsuse other types of math thatexperts believe will be hard to solve for quantum computers and conventional computers alike.

Additional algorithms still under consideration are designed for general encryption and do not use structured lattices or hash functions in their approaches.

To put these algorithms into practice, NIST has led efforts to develop technical standards for post-quantum encryption. These standards aim to provide solutions for different situations, employ varied approaches for encryption, and offer more than one algorithm for each kind of application in the event one proves vulnerable.

## When will a quantum computer appear that is powerful enough to threaten current encryption methods?

No one knows. Researchers need to surmount many technical challenges before this can happen. Experts’ estimates range from a few years to a few decades.

The basic unit of information in a quantum computer is called a quantum bit, or “qubit.” Qubits are quantum computing’s equivalent of a bit in a conventional computer. Quantum computers employing many thousands of qubits will be needed to break present-day encryption.

There is a fundamental problem: Qubits are fragile. The slightest disturbances can corrupt them and create errors before a quantum computer can successfully complete an operation, such as breaking an encryption code.

Researchers are experimenting with [different technologies for making qubits](/quantum-information-science/quantum-computing-explained). Each type has advantages and disadvantages, and nobody is sure which approach will end up working best — or if some other approach, yet to be discovered, will overtake them all.

Still, even though it’s not possible to predict exactly when — or even if — quantum computers will break present-day encryption, the potential threat is great enough that researchers are preparing for it now.

## If cryptographically relevant quantum computers don’t exist yet, why is developing post-quantum encryption algorithms important now?

The world must plan ahead. Historically, it has taken a long time from the moment that a new algorithm is standardized until it is fully integrated into information systems. The process can take 10 to 20 years, partly because companies have to respond to the changes by building the algorithms into products and services we use every day.

No one knows how long it will take to build a cryptographically relevant quantum computer. Predictions vary widely, but some people think it may be possible in less than 10 years.

Even if computer security experts implement post-quantum encryption algorithms before sufficiently powerful quantum computers are built, a lot of encrypted data remains under threat because of a type of attack called “harvest now, decrypt later.”

## What is “harvest now, decrypt later”?

Some secrets remain valuable for many years. Even if an adversary can’t crack the encryption that protects our secrets at the moment, it could still be beneficial to capture encrypted data and hold onto it, in the hopes that a quantum computer will break the encryption down the road. This idea is sometimes expressed as “harvest now, decrypt later” — and it’s one of the reasons computers need to start encrypting data with post-quantum techniques as soon as possible.

## How did NIST design and select the algorithms it is standardizing?

NIST kicked off the Post-Quantum Cryptography project[in 2016](/news-events/news/2016/04/nist-kicks-effort-defend-encrypted-data-quantum-computer-threat)and late that year[formally asked](/news-events/news/2016/12/nist-asks-public-help-future-proof-electronic-information)the world’s cryptography experts to submit algorithms that would prove intractable to both classical and quantum computers. By the deadline about a year later, experts from dozens of countries had submitted 69 candidate algorithms that cleared the bar NIST had set.

NIST then released the 69 candidate algorithms for experts to analyze and crack if they could. This process was open and transparent.Over the next several yearsmany of the world’s best cryptographers participated in[multiple rounds of evaluation](/news-events/news/2020/07/nists-post-quantum-cryptography-program-enters-selection-round), which reduced the number of candidates.

NIST has encouraged the world’s cryptographers to look at how the candidate algorithms work not only in big computers and smartphones, but also in devices that have limited processor power. Smart cards, tiny devices such as smart kitchen appliances for use in the Internet of Things, and individual microchips all need quantum-resistant algorithms too.

## Why is NIST leading the effort to develop PQC standards?

NIST has [extensive experience](/cryptography) developing encryption algorithms. NIST has fostered the development of cryptographic techniques and technology for 50 years through an open process that brings together industry, government and academia to develop workable approaches to cryptographic protection that enable practical security.

NIST develops guidance by involving the public to work with NIST’s own accomplished experts. All development steps happen in the public eye, generally with numerous opportunities for interested parties to comment on the proceedings.

Part of the agency’s mission is to develop standards that will prove broadly useful to everyone, not just a particular company or group. When the post-quantum encryption standards are complete, they will be adopted by federal agencies and released for free public use.

## What can we be doing now to get ready for cryptographically relevant quantum computers?

We now have post-quantum encryption algorithms that are ready for use. NIST [released the first three finalized PQC standards](/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards) that incorporate them in 2024.

“We encourage organizations to begin their transition to these standards immediately to ensure their data remains secure in the quantum era,” said NIST mathematician Dustin Moody, who heads the PQC standardization project.

Technology managers can inventory their systems for applications that use encryption, which will need to be replaced before cryptographically relevant quantum computers appear. They can also alert their tech departments and vendors about the upcoming change.

To learn more about migrating to post-quantum cryptography, and to get involved in developing guidance, see[NIST’s National Cybersecurity Center of Excellence project page](https://www.nccoe.nist.gov/crypto-agility-considerations-migrating-post-quantum-cryptographic-algorithms).

## How does post-quantum cryptography differ from quantum cryptography?

Though their names sound the same, they are very different. Post-quantum cryptography is a defense against potential cyberattacks from quantum computers. PQC algorithms are based on mathematical techniques that can be very old, such as elliptic curves, which trace their history back to[ancient Greek times](https://www.maths.tcd.ie/pub/Maths/Courseware/499/2006/Mars/ellcurves.pdf).

Quantum cryptography, on the other hand, is based fundamentally on quantum physics, which originated in the 20th century. Quantum cryptography uses the counterintuitive properties of quantum mechanics to create new forms of secure encryption. Like PQC, it is also expected to be resistant to attacks from quantum computers, but in a different way.[**Learn more about quantum cryptography.**](/cybersecurity-and-privacy/what-quantum-cryptography)
