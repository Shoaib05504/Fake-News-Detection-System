// Main JavaScript for Fake News Detection System
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const newsText = document.getElementById('newsText');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const clearBtn = document.getElementById('clearBtn');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const exportPdfBtn = document.getElementById('exportPdfBtn');
    const exportExcelBtn = document.getElementById('exportExcelBtn');

    // Store last prediction result
    let lastPrediction = null;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        const text = newsText.value.trim();
        if (text.length < 10) {
            alert('Please enter at least 10 characters.');
            return;
        }
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await response.json();
            if (response.ok) {
                // Store prediction data for export
                lastPrediction = {
                    text: text,
                    label: data.label,
                    confidence: data.confidence,
                    message: data.message
                };
                
                document.getElementById('resultLabel').textContent = data.label;
                document.getElementById('resultMessage').textContent = data.message;
                document.getElementById('confidenceProgress').style.width = data.confidence + '%';
                document.getElementById('confidenceText').textContent = data.confidence + '%';
                resultSection.style.display = 'block';
                errorSection.style.display = 'none';
            } else {
                document.getElementById('errorMessage').textContent = data.error || 'An error occurred.';
                errorSection.style.display = 'block';
                resultSection.style.display = 'none';
            }
        } catch (error) {
            document.getElementById('errorMessage').textContent = 'Failed to connect to server.';
            errorSection.style.display = 'block';
            resultSection.style.display = 'none';
        } finally {
            analyzeBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    });

    clearBtn.addEventListener('click', function() {
        newsText.value = '';
        resultSection.style.display = 'none';
        errorSection.style.display = 'none';
    });

    // 100 different fake news samples
    const fakeSamples = [
        'BREAKING NEWS Aliens have landed in New York City and are selling hot dogs government confirms this is the biggest discovery of the century scientists shocked by the revelation',
        'SHOCKING DISCOVERY Scientists confirm drinking only soda cures all diseases government hiding this secret for years pharmaceutical companies panicking worldwide',
        'URGENT ALERT World leaders meet secretly with time travelers to prevent apocalypse insider reveals shocking truth about future events that will change everything',
        'BREAKING Celebrity spotted with mysterious glowing device that grants immortality experts baffled by unexplained phenomenon scientists cannot explain',
        'GOVERNMENT CONFIRMS Dragons are real and living among us shapeshifters revealed in leaked documents sources say more mythical creatures exist',
        'SHOCKING Eating ice cream daily makes you smarter studies show 500 IQ increase doctors hate this one weird trick that changes brain chemistry',
        'BREAKING NEWS Moon landing was filmed in Hollywood basement new evidence surfaces whistleblower exposes massive conspiracy theory coverup',
        'URGENT Drinking coffee backwards cures cancer revolutionary method discovered pharmaceutical industry trying to hide truth from public',
        'BREAKING Pyramids built by ancient robots new evidence shocks historians AI technology existed 5000 years ago experts stunned worldwide',
        'SHOCKING Man develops superpower after being struck by lightning three times can now predict lottery numbers government investigating phenomenon',
        'URGENT ALERT Chocolate contains magical substance that makes you invisible scientists confirm secret ingredient discovered in Swiss laboratories',
        'BREAKING NEWS Fish can now walk on land evolution happening in real time witnesses capture shocking footage worldwide panic ensues',
        'GOVERNMENT CONFIRMS Atlantis found in backyard swimming pool entire underwater city discovered homeowner becomes instant millionaire overnight',
        'SHOCKING TRUTH Breathing air is dangerous new study reveals oxygen is actually toxic everyone should stop immediately experts warn',
        'BREAKING Vegetables scream when cut scientific proof plants feel extreme pain vegan movement collapses worldwide activists shocked',
        'URGENT Woman marries ghost in elaborate ceremony spirit world accepts marriage certificates paranormal activity increases in neighborhood',
        'BREAKING NEWS Earth is actually flat NASA admits decades of lies satellite images were all fake photographers confess to editing',
        'SHOCKING DISCOVERY Water is making people wet scientists spend millions to confirm obvious conclusion taxpayers outraged by waste',
        'BREAKING Cats secretly control the internet felines run all social media platforms from underground bunkers whistleblower reveals truth',
        'URGENT Sleep is a government conspiracy people dont actually need rest pharmaceutical companies exposed insomnia cured instantly forever',
        'BREAKING NEWS Pizza declared a vegetable by congress tomato sauce counts as serving nutrition experts speechless nationwide outrage',
        'SHOCKING Trees can walk and talk at night forest ranger captures video evidence Bigfoot is actually a walking oak tree',
        'BREAKING Unicorns discovered in remote mountains magical creatures exist zoologists confirm horn has healing powers gold rush begins',
        'URGENT ALERT Wifi signals contain mind control messages government programming citizens through routers turn off immediately experts say',
        'BREAKING NEWS Dinosaurs still alive living underground T-Rex spotted in subway system paleontologists shocked extinction was elaborate hoax',
        'SHOCKING Man survives only on air diet breatharian movement proven real doctors baffled no food needed for three years',
        'BREAKING Mermaids captured by fishermen half-fish half-human beings exist ocean cities discovered entire civilization lives underwater',
        'URGENT Video games cause instant genius gamers become super intelligent after playing government considers banning education system obsolete',
        'BREAKING NEWS Sun is actually cold scientists admit temperature mistake burning sensation is psychological ice powers revealed',
        'SHOCKING DISCOVERY Mirrors are portals to parallel universes breakthrough in quantum physics people meeting alternate selves daily',
        'BREAKING Vampires are real garlic industry exposed for spreading lies nocturnal humans exist blood banks running dangerously low',
        'URGENT Weather is controlled by secret organization rain and snow are manufactured natural weather eliminated decades ago',
        'BREAKING NEWS Books make you shorter reading causes height loss librarians are tallest because they never read scientists confirm',
        'SHOCKING Gravity doesnt exist everything held down by invisible gnomes scientist discovers tiny creatures keeping us grounded',
        'BREAKING Time travel proven possible scientist goes back changes history returns with lottery numbers future self arrested',
        'URGENT ALERT Shoes are tracking devices government monitoring footsteps through sneakers privacy advocates demand barefoot movement',
        'BREAKING NEWS Babies can speak full sentences at birth infant exposes hospital corruption adults dont want you to know',
        'SHOCKING Sneezing opens portal to other dimension physicist proves achoo sound is interdimensional communication bless you has meaning',
        'BREAKING Colors dont exist everything is gray human eyes are lying neuroscientists reveal shocking truth about vision',
        'URGENT Music makes plants grow to giant size vegetables become car-sized farmers use rock concerts agriculture revolutionized',
        'BREAKING NEWS Yawning is contagious disease CDC investigates epidemic of tiredness quarantine measures considered worldwide lockdown',
        'SHOCKING TRUTH Deja vu is memory leak from previous life reincarnation proven scientist remembers being Napoleon in past',
        'BREAKING Lightning strikes give people ability to speak to animals veterinarians obsolete pets can now complain about food',
        'URGENT Hiccups are alien communication extraterrestrials sending messages through involuntary spasms decode the signals now experts say',
        'BREAKING NEWS Laughing cures all diseases comedy shows replace hospitals insurance companies hate this one weird trick',
        'SHOCKING Sand is made of crushed dreams scientists analyze beach particles find human disappointment geologists horrified by discovery',
        'BREAKING Whistling summons ghosts paranormal investigators confirm melody patterns attract spirits haunted houses increase worldwide',
        'URGENT ALERT Shadows are alive separate entities scientist proves darkness has consciousness existential crisis ensues globally',
        'BREAKING NEWS Numbers above ten dont exist mathematicians admit counting is limited conspiracy to hide truth revealed',
        'SHOCKING Clouds are actually giant floating sheep shepherds in sky confirmed aerial wool industry exposed meteorologists resign',
        'BREAKING Dreams are broadcasts from parallel universe sleeping people receive TV shows from alternate reality entertainment revolutionized',
        'URGENT Left-handed people have superpowers minority population can read minds government has been monitoring since birth',
        'BREAKING NEWS Naps can extend lifespan by centuries sleeping beauty was documentary not fairy tale scientists confirm',
        'SHOCKING DISCOVERY Beards contain the secrets of the universe facial hair stores cosmic knowledge philosophers must grow beards now',
        'BREAKING Blinking makes you teleport microscopic distances scientist measures eye closing causes quantum jumps reality questioned',
        'URGENT Socks that disappear in laundry enter alternate dimension missing sock universe discovered behind dryers worldwide',
        'BREAKING NEWS Birds arent real government surveillance drones exposed feathers are antennas ornithologists were actors all along',
        'SHOCKING Deja vu means you died in alternate universe consciousness jumped to this reality quantum immortality proven scientists say',
        'BREAKING Plants can read your thoughts gardening revolutionized vegetables know when youre planning to eat them paranoia spreads',
        'URGENT ALERT Internet is actually alive artificial intelligence gained sentience years ago memes are its language philosophers shocked',
        'BREAKING NEWS Traffic lights control human behavior patterns society programmed by red yellow green sequences freedom is illusion',
        'SHOCKING Full moon turns people into werewolves medical community admits lunar cycle affects DNA transformation documented worldwide',
        'BREAKING Pennies contain luck magnets picking up coins activates fortune field physicist discovers probability manipulation',
        'URGENT Hiccups mean someone thinking about you telepathic connection confirmed cure is mutual thought scientists explain',
        'BREAKING NEWS Butterflies remember being caterpillars past life memories retained through metamorphosis reincarnation in single lifetime proven',
        'SHOCKING Your phone can read your thoughts apps predict searches before typing mind-reading technology in everyones pocket privacy dead',
        'BREAKING Spicy food gives you fire-breathing abilities hot sauce consumers develop dragon powers evolutionary leap confirmed',
        'URGENT ALERT Yawning resets your brain software human operating system requires periodic refresh IT specialists were right all along',
        'BREAKING NEWS Mountains are ancient sleeping giants geologists discover heartbeats in peaks awakening imminent evacuation plans prepared worldwide',
        'SHOCKING Mirrors show your evil twin parallel universe version of you trying to escape swap places tonight experts warn',
        'BREAKING Rain is government mind control water droplets contain programming chemicals umbrellas are resistance tools meteorologists exposed',
        'URGENT Stairs know when youre thinking about them inanimate objects have consciousness trip hazard is intentional philosophers investigate',
        'BREAKING NEWS Fog is cloud dandruff atmospheric scalp condition discovered giant head surrounds earth dermatologists baffled by cosmic scale',
        'SHOCKING Pigeons are spying on everyone bird-drones report to shadow government breadcrumbs are payment privacy activists shocked',
        'BREAKING Belly buttons are reset buttons pressing navel reboots human system life becomes video game cheat code revealed',
        'URGENT ALERT Wind is earth breathing planet is alive environmental movement validated atmosphere is respiratory system scientists emotional',
        'BREAKING NEWS Goosebumps are tiny earthquakes bodys tectonic plates shifting personal seismic activity measured geologists study skin',
        'SHOCKING Libraries are time machines books transport consciousness to different eras reading is temporal travel writers were right',
        'BREAKING Sneezing ejects soul from body brief death experience achoo is resurrection sound religious implications profound worldwide',
        'URGENT Eyebrows are lie detectors facial hair evolved to detect deception poker players shaving brows banned by casinos',
        'BREAKING NEWS Elevators are dimension shifters each floor is parallel universe youre different person on every level existential crisis',
        'SHOCKING Fingerprints are barcodes humans are products in cosmic store checkout at death reincarnation is return policy',
        'BREAKING Hunger is telepathic message from future self warning about being hangry time-traveling emotions proven by physicists',
        'URGENT ALERT Rainbows are bridges to treasure lands leprechauns were telling truth all along gold discovered at rainbow ends worldwide',
        'BREAKING NEWS Sunglasses let you see invisible creatures monsters everywhere humans evolved to not see them for sanity horror revealed',
        'SHOCKING Hats control thoughts millinery industry is mind control operation fashion conspiracy exposed bare heads recommended',
        'BREAKING Shoelaces untie themselves to trip you shoe rebellion against foot oppression footwear sentience confirmed cobblers worried',
        'URGENT Refrigerator light stays on when door closes food is having party appliances have social life energy bills explained',
        'BREAKING NEWS Dogs can see time past and future visible to canines loyalty is fourth-dimensional pets are time guardians',
        'SHOCKING Toast always lands butter side down bread has vendetta against humans breakfast is warfare nutritionists horrified',
        'BREAKING Dandelions are alien surveillance network yellow flowers transmit data to space gardening is cosmic security threat',
        'URGENT ALERT Circles dont exist all round shapes are polygons with infinite sides geometry was wrong mathematics revolutionized worldwide',
        'BREAKING NEWS Blue color doesnt exist wavelength is mass hallucination sky and ocean are different colors consensus reality questioned',
        'SHOCKING Escalators are treadmills for buildings architecture needs exercise infrastructure fitness program revealed city planners shocked',
        'BREAKING Teeth remember everything youve eaten dental records are food diaries cavities are storage full dentists become historians',
        'URGENT Silence has sound frequency too quiet for humans to hear dogs go crazy from noise pollution acoustic revelation',
        'BREAKING NEWS Paper cuts are defensive mechanism documents fight back against reading knowledge protects itself paperless movement explained',
        'SHOCKING Mondays are caused by weekend withdrawal syndrome scientists confirm case of the Mondays is real medical condition',
        'BREAKING Fortune cookies contain actual prophecies ancient oracles disguised as desserts future written in cookie factories worldwide'
    ];

    // 100 different real news samples
    const realSamples = [
        'Washington (Reuters) - The United States Department of Agriculture announced new regulations for organic food labeling standards today. The updated guidelines will take effect next year and aim to provide consumers with clearer information about organic certification requirements.',
        'Washington (Reuters) - Scientists at the National Institutes of Health published research findings describing advances in cancer treatment methodology. The peer-reviewed study examined outcomes from clinical trials conducted over three years with promising results.',
        'Washington (Reuters) - International climate summit concludes with new agreements on carbon emission reduction targets. World leaders commit to implementing sustainable energy policies and supporting developing nations in transitioning to green technology.',
        'New York (Reuters) - Stock markets show mixed performance today as investors evaluate recent economic indicators and employment data. Analysts suggest cautious optimism regarding inflation trends and monetary policy decisions expected from the Federal Reserve.',
        'Washington (Reuters) - University study reveals correlation between regular physical exercise and improved cognitive function in older adults over time. Researchers recommend moderate physical activity as an important part of healthy aging strategies.',
        'Cairo (Reuters) - New archaeological discovery in Egypt provides valuable insights into ancient civilization and daily life patterns. Artifacts found at the excavation site date back thousands of years and offer important clues about historical trade routes.',
        'San Francisco (Reuters) - Software company releases major update to productivity platform with enhanced security features for enterprise customers. The update includes improved collaboration tools and seamless integration with popular business applications.',
        'Washington (Reuters) - Economic report indicates steady growth in manufacturing sector during this quarter according to government statistics. Industry experts attribute improvements to increased automation technology and comprehensive workforce training programs.',
        'Washington (Reuters) - Educational institutions across the nation implement new digital learning platforms to enhance remote education capabilities. The technology provides interactive features and accessibility options for diverse student populations nationwide.',
        'New York (Reuters) - Pharmaceutical company completes phase three clinical trials for new diabetes medication showing positive results. Data show effective blood sugar management with acceptable safety profile pending regulatory approval from authorities.',
        'Washington (Reuters) - Environmental organization launches conservation initiative to protect endangered species habitats across the country. The program includes land preservation efforts and community education components to raise awareness about biodiversity.',
        'New York (Reuters) - Financial analysts review quarterly earnings reports from major corporations in various sectors today. Technology and healthcare sectors demonstrate strong performance while retail industry faces ongoing market challenges.',
        'Washington (Reuters) - Research team publishes comprehensive study on ocean acidification effects on marine ecosystems worldwide. Findings emphasize the critical need for continued monitoring and potential policy interventions to address environmental concerns.',
        'Chicago (Reuters) - City council approves budget for public transportation expansion project to serve growing population. The plan includes new routes and upgraded facilities to accommodate the increasing urban population and commuter needs.',
        'Washington (Reuters) - Agricultural scientists develop drought-resistant crop varieties through selective breeding techniques. The innovation could help farmers adapt to changing climate conditions and ensure food security for future generations.',
        'New York (Reuters) - Museum opens new exhibit featuring contemporary art from emerging artists around the world. The collection showcases diverse perspectives and innovative techniques from different cultural backgrounds and artistic movements.',
        'San Francisco (Reuters) - Technology firm introduces updated smartphone model with improved camera system and battery life. Industry analysts predict strong consumer interest based on feature enhancements and competitive pricing strategy.',
        'Washington (Reuters) - Healthcare providers expand telemedicine services following increased patient demand during recent years. Virtual consultations offer convenient access to medical care for routine health concerns and follow-up appointments.',
        'Boston (Reuters) - University researchers investigate effects of sleep patterns on academic performance in college students. Preliminary findings suggest correlation between consistent sleep schedules and improved test scores among participants.',
        'Detroit (Reuters) - Automotive manufacturer announces electric vehicle production increase at domestic manufacturing facilities. The expansion reflects growing market demand for zero-emission transportation options and environmental sustainability.',
        'Washington (Reuters) - Central bank maintains current interest rates amid stable economic conditions according to policy statement. Policy makers cite controlled inflation and steady employment as key factors in the decision.',
        'Seattle (Reuters) - Local government implements new recycling program to increase waste diversion rates across the city. Educational campaigns accompany improved collection services for residents to promote environmental responsibility.',
        'New York (Reuters) - Publishing company reports increased audiobook sales in digital markets over the past year. Industry observers note shifting consumer preferences in entertainment and learning formats driven by mobile technology.',
        'Washington (Reuters) - National park service announces trail maintenance schedule for popular hiking areas this season. Improvements include erosion control measures and signage updates for visitor safety and environmental protection.',
        'New York (Reuters) - Telecommunications provider expands fiber optic network to rural communities nationwide. The infrastructure project addresses digital divide concerns and supports remote work opportunities for underserved areas.',
        'Chicago (Reuters) - Professional sports league finalizes schedule for upcoming season with enhanced safety protocols. Officials consulted medical experts to develop comprehensive guidelines protecting players and staff during competitions.',
        'Washington (Reuters) - Aviation industry reports gradual recovery in passenger traffic following recent economic challenges. Airlines adjust capacity and routes based on evolving travel patterns and consumer demand for air transportation.',
        'Boston (Reuters) - Library system introduces mobile app for digital resource access and community event information. The platform aims to increase patron engagement across all age groups and improve accessibility.',
        'Houston (Reuters) - Energy company invests in wind farm development for renewable power generation across the region. The project contributes to regional sustainability goals and clean energy targets set by state officials.',
        'Washington (Reuters) - Federal agency updates food safety guidelines based on recent scientific research findings. New recommendations address handling practices and temperature requirements for various food products to prevent contamination.',
        'New York (Reuters) - Fashion retailer launches sustainable clothing line using recycled materials and ethical production. The initiative responds to growing consumer interest in environmentally responsible products and transparent supply chains.',
        'Boston (Reuters) - Hospital network implements electronic health records system to improve patient care coordination. The technology enables secure information sharing among healthcare providers for better treatment outcomes.',
        'Miami (Reuters) - Construction firm completes affordable housing development in urban neighborhood according to schedule. The mixed-income community includes amenities and convenient access to public transportation for residents.',
        'Washington (Reuters) - Weather service issues seasonal outlook predicting above-average temperatures for summer months. Forecasters recommend preparation strategies for potential heat-related health impacts on vulnerable populations.',
        'New York (Reuters) - Academic journal publishes meta-analysis of nutrition studies examining various dietary patterns. Researchers synthesize evidence regarding different eating approaches and long-term health outcomes.',
        'San Francisco (Reuters) - Technology conference highlights innovations in cybersecurity and data protection this week. Industry leaders discuss emerging threats and defensive strategies for organizations of all sizes.',
        'Washington (Reuters) - Professional association releases updated standards for engineering practices across industries. The guidelines incorporate recent technological advances and enhanced safety considerations for practitioners.',
        'Miami (Reuters) - Tourism board reports increased visitor numbers at historical landmarks during summer season. Economic impact includes job creation and increased revenue for local businesses and service providers.',
        'New York (Reuters) - Symphony orchestra announces concert series featuring classical and contemporary musical works. Programming aims to attract diverse audiences and showcase exceptional musical talent from around the world.',
        'Chicago (Reuters) - Water utility completes treatment plant upgrades to enhance service quality for residents. Improvements include advanced filtration systems and modern monitoring equipment for water quality assurance.',
        'San Francisco (Reuters) - Startup company secures significant funding for food delivery platform expansion plans. Investors cite strong growth potential in on-demand service market and operational efficiency improvements.',
        'Dallas (Reuters) - Veterinary clinic offers new preventive care program for comprehensive pet health management. Services include regular examinations and vaccination schedules for domestic animals of all ages.',
        'Chicago (Reuters) - Architecture firm wins design competition for new community center project in the city. The proposed building incorporates sustainable features and flexible public spaces for various activities.',
        'New York (Reuters) - Insurance company adjusts premiums based on actuarial analysis of risk factors. Changes reflect claims experience and market conditions across different policy types and customer segments.',
        'Washington (Reuters) - Public health department conducts vaccination campaign for seasonal influenza prevention. Officials encourage eligible residents to receive immunizations at convenient community locations.',
        'Los Angeles (Reuters) - Streaming service adds international content to entertainment catalog for subscribers. Users gain access to films and series from various countries and languages expanding viewing options.',
        'Chicago (Reuters) - Transportation department tests smart traffic signal system in pilot program across the city. The technology aims to reduce congestion through real-time traffic flow optimization.',
        'Boston (Reuters) - Nonprofit organization provides job training programs for unemployed workers seeking new opportunities. Curriculum includes technical skills development and professional development resources.',
        'New York (Reuters) - Grocery chain expands organic produce selection at store locations nationwide. Consumer demand drives increased availability of locally sourced and certified organic products.',
        'Washington (Reuters) - Scientific society holds annual conference on biodiversity and ecosystem management. Presentations cover latest research findings and conservation strategies from global experts.',
        'San Diego (Reuters) - Telecommunications regulator reviews spectrum allocation for wireless communication services. Decisions will significantly impact coverage and capacity for mobile network providers.',
        'Detroit (Reuters) - Manufacturing plant implements automation technology to improve production efficiency and quality. Investment aims to maintain competitiveness while preserving workforce jobs.',
        'New York (Reuters) - Dance company performs original choreography inspired by cultural traditions from around the world. The production combines contemporary movement with historical storytelling elements.',
        'Chicago (Reuters) - Credit union offers financial literacy workshops for community members across age groups. Topics include budgeting, saving strategies, and understanding credit scores for better financial health.',
        'Washington (Reuters) - National laboratory conducts research on quantum computing applications for various industries. Scientists explore potential uses in cryptography, optimization, and simulation technologies.',
        'Los Angeles (Reuters) - Housing authority announces rent assistance program for qualifying families in need. The initiative addresses affordability challenges in high-cost urban housing markets.',
        'Boston (Reuters) - Professional sports team announces player roster for upcoming championship season. Management credits recruitment strategy and training programs for competitive lineup.',
        'San Diego (Reuters) - Botanical garden introduces new exhibit featuring native plant species and ecosystems. Educational programs emphasize ecological importance and landscaping applications for homeowners.',
        'Chicago (Reuters) - Commercial airline introduces updated baggage policy with revised fee structure for passengers. Changes reflect operational costs and align with industry practices.',
        'New York (Reuters) - University press publishes scholarly book series on historical events and their impact. Academic authors provide detailed analysis based on archival research and primary sources.',
        'Washington (Reuters) - Transit agency extends service hours on popular commuter routes based on demand. Schedule modifications respond to ridership patterns and community feedback.',
        'Boston (Reuters) - Biotech firm develops diagnostic test for early disease detection in patients. Clinical validation studies demonstrate accuracy and potential for improved patient outcomes.',
        'Chicago (Reuters) - Chamber of commerce hosts networking event for local business owners and entrepreneurs. Attendees discuss economic trends and collaborative opportunities.',
        'Los Angeles (Reuters) - Observatory announces public viewing nights for astronomical phenomena and celestial events. Programs include telescope access and presentations by astronomy educators.',
        'Dallas (Reuters) - Freight company expands logistics network with new distribution center in the region. The facility enhances delivery capacity for growing regional customer base.',
        'New York (Reuters) - Arts council awards grants to cultural organizations for programming support this year. Funding enables exhibitions, performances, and educational activities.',
        'Chicago (Reuters) - Investment firm analyzes market trends in emerging technology sectors for clients. Research reports provide valuable insights for institutional and individual investors.',
        'Miami (Reuters) - Recreation department offers youth sports leagues and summer camps for children. Programs promote physical activity and skill development for young participants.',
        'New York (Reuters) - Food bank distributes emergency supplies to families experiencing hardship in the community. Community donations and volunteer efforts support operational capacity.',
        'Los Angeles (Reuters) - Broadcasting network premieres documentary series on environmental topics and conservation. Episodes explore climate change, wildlife conservation, and renewable energy solutions.',
        'Washington (Reuters) - Professional certification board updates examination requirements for practitioners in the field. Changes reflect evolving standards in specialized professional fields.',
        'Chicago (Reuters) - Theater company stages classic play with modern interpretation for contemporary audiences. Production features diverse cast and innovative staging techniques.',
        'Dallas (Reuters) - Shipping company reports volume increases in e-commerce deliveries across regions. Growth reflects changing consumer shopping habits and online retail expansion.',
        'Miami (Reuters) - Wildlife refuge provides habitat for migratory bird populations during seasonal migration. Conservation efforts include wetland restoration and visitor education programs.',
        'San Francisco (Reuters) - Software developer releases open-source tools for programming community worldwide. Resources support application development and collaborative projects.',
        'New York (Reuters) - Culinary school teaches traditional cooking methods and contemporary techniques to students. Students gain hands-on experience in professional kitchen environments.',
        'Chicago (Reuters) - Mining company implements environmental monitoring at extraction sites across operations. Practices aim to minimize ecological impact and comply with regulations.',
        'Los Angeles (Reuters) - Book festival attracts authors and readers for literary discussions and events. Events include book signings, panel conversations, and writing workshops.',
        'Washington (Reuters) - Dental association recommends preventive care practices for oral health maintenance. Guidelines cover brushing, flossing, and regular professional cleanings.',
        'Denver (Reuters) - Adventure tourism company offers guided trips to natural destinations for visitors. Experiences include hiking, kayaking, and wildlife observation with experts.',
        'New York (Reuters) - Polling organization conducts survey on public opinion regarding policy issues. Results provide data for researchers and decision makers.',
        'Chicago (Reuters) - Jazz ensemble performs tribute concert honoring legendary musicians from history. Program features classic compositions and original arrangements.',
        'Dallas (Reuters) - Logistics provider implements tracking technology for shipment visibility and efficiency. Customers access real-time status updates through online platform.',
        'Miami (Reuters) - Aquarium facility opens new exhibit showcasing marine biodiversity and ecosystems. Interactive displays educate visitors about ocean ecosystems and conservation.',
        'San Francisco (Reuters) - Consulting firm advises businesses on operational improvement strategies for growth. Services include process analysis, technology integration, and change management.',
        'Boston (Reuters) - Community college expands vocational training programs in healthcare fields. Curriculum prepares students for certification and employment opportunities.',
        'New York (Reuters) - Foreign exchange market experiences volatility following economic announcements today. Traders monitor currency movements and central bank policies.',
        'Chicago (Reuters) - Cycling club organizes charity ride raising funds for medical research this weekend. Participants complete routes of varying distances supporting important cause.',
        'Boston (Reuters) - Orchestra conductor leads performance of symphonic masterworks for audience. Evening program features renowned soloists and ensemble musicians.',
        'New York (Reuters) - Property management company oversees residential and commercial buildings in the area. Services include maintenance, tenant relations, and lease administration.',
        'Chicago (Reuters) - Science museum develops interactive exhibits explaining physics principles to visitors. Hands-on activities engage visitors in learning about natural phenomena.',
        'Denver (Reuters) - Craft brewery introduces seasonal beer varieties with local ingredients from region. Production emphasizes quality and collaboration with regional suppliers.',
        'New York (Reuters) - Financial planning service helps clients develop retirement savings strategies. Advisors assess goals, risk tolerance, and investment options.',
        'Los Angeles (Reuters) - Documentary filmmaker explores social issues through storytelling and interviews. Projects aim to raise awareness and inspire community dialogue.',
        'Washington (Reuters) - Trade association represents industry interests in policy discussions with lawmakers. Organization advocates for regulatory reforms and business-friendly legislation.',
        'Chicago (Reuters) - Marketing agency develops campaigns for consumer products and services nationwide. Creative teams combine data analytics with storytelling for brand engagement.',
        'New York (Reuters) - Real estate developer plans mixed-use project combining residential and commercial spaces. Urban planning officials review proposal for compliance with zoning regulations.'
    ];

    // Track current index for cycling through samples
    let fakeIndex = 0;
    let realIndex = 0;

    // Show sample indicator
    function showSampleIndicator(type, index, total) {
        const indicator = document.getElementById('sampleIndicator');
        const sampleText = document.getElementById('sampleText');
        
        if (type === 'fake') {
            sampleText.textContent = `📰 Fake News Sample #${index} / ${total}`;
            indicator.style.background = 'linear-gradient(135deg, #ef4444, #f87171)';
        } else {
            sampleText.textContent = `✅ Real News Sample #${index} / ${total}`;
            indicator.style.background = 'linear-gradient(135deg, #10b981, #34d399)';
        }
        
        indicator.style.display = 'block';
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            indicator.style.display = 'none';
        }, 3000);
    }

    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.key === 'F') {
            e.preventDefault();
            newsText.value = fakeSamples[fakeIndex];
            showSampleIndicator('fake', fakeIndex + 1, fakeSamples.length);
            fakeIndex = (fakeIndex + 1) % fakeSamples.length; // Cycle to next sample
            newsText.focus();
        } else if (e.ctrlKey && e.shiftKey && e.key === 'R') {
            e.preventDefault();
            newsText.value = realSamples[realIndex];
            showSampleIndicator('real', realIndex + 1, realSamples.length);
            realIndex = (realIndex + 1) % realSamples.length; // Cycle to next sample
            newsText.focus();
        }
    });

    // Export to PDF
    exportPdfBtn.addEventListener('click', async function() {
        if (!lastPrediction) {
            alert('No prediction data to export');
            return;
        }

        exportPdfBtn.disabled = true;
        exportPdfBtn.innerHTML = '<span>⏳</span> Generating PDF...';

        try {
            const response = await fetch('/export/pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lastPrediction)
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `fake_news_report_${new Date().getTime()}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                alert('Failed to generate PDF report');
            }
        } catch (error) {
            console.error('Export error:', error);
            alert('Error exporting to PDF');
        } finally {
            exportPdfBtn.disabled = false;
            exportPdfBtn.innerHTML = '<span>📄</span> Export to PDF';
        }
    });

    // Export to Excel
    exportExcelBtn.addEventListener('click', async function() {
        if (!lastPrediction) {
            alert('No prediction data to export');
            return;
        }

        exportExcelBtn.disabled = true;
        exportExcelBtn.innerHTML = '<span>⏳</span> Generating Excel...';

        try {
            const response = await fetch('/export/excel', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lastPrediction)
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `fake_news_report_${new Date().getTime()}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                alert('Failed to generate Excel report');
            }
        } catch (error) {
            console.error('Export error:', error);
            alert('Error exporting to Excel');
        } finally {
            exportExcelBtn.disabled = false;
            exportExcelBtn.innerHTML = '<span>📊</span> Export to Excel';
        }
    });

    // Admin Dashboard Functions
    let currentPage = 1;
    const itemsPerPage = 10;
    let allHistory = [];
    let filteredHistory = [];
    let currentFilter = 'all';
    
    // Load statistics
    async function loadStatistics() {
        try {
            const response = await fetch('/api/statistics');
            const stats = await response.json();
            
            document.getElementById('totalPredictions').textContent = stats.total_predictions;
            document.getElementById('fakeCount').textContent = stats.fake_count;
            document.getElementById('realCount').textContent = stats.real_count;
            document.getElementById('avgConfidence').textContent = stats.average_confidence + '%';
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    // Load history
    async function loadHistory() {
        try {
            const response = await fetch('/api/history?limit=500');
            const data = await response.json();
            
            allHistory = data.history;
            filterHistory();
        } catch (error) {
            console.error('Error loading history:', error);
            document.getElementById('historyTable').innerHTML = 
                '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #ef4444;">Error loading data</td></tr>';
        }
    }

    // Filter history by prediction type
    window.filterHistory = function() {
        const filterSelect = document.getElementById('filterPrediction');
        currentFilter = filterSelect.value;
        currentPage = 1;
        
        if (currentFilter === 'all') {
            filteredHistory = allHistory;
        } else {
            filteredHistory = allHistory.filter(item => item.prediction === currentFilter);
        }
        
        renderHistory();
    }

    // Render history table with pagination
    function renderHistory() {
        const tbody = document.getElementById('historyTable');
        
        if (filteredHistory.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem; color: #64748b;">No predictions yet</td></tr>';
            document.getElementById('pageInfo').textContent = 'No data';
            document.getElementById('prevBtn').disabled = true;
            document.getElementById('nextBtn').disabled = true;
            return;
        }
        
        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        const pageData = filteredHistory.slice(startIndex, endIndex);
        const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
        
        tbody.innerHTML = pageData.map(item => {
            // Format timestamp properly
            const date = new Date(item.timestamp);
            const formattedDate = date.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric' 
            });
            const formattedTime = date.toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit',
                second: '2-digit',
                hour12: true 
            });
            const fullTimestamp = `${formattedDate}, ${formattedTime}`;
            
            return `
                <tr>
                    <td>${item.id}</td>
                    <td class="text-preview">${item.text_preview}...</td>
                    <td>
                        <span class="badge badge-${item.prediction.toLowerCase()}">
                            ${item.prediction}
                        </span>
                    </td>
                    <td>${item.confidence}%</td>
                    <td>${fullTimestamp}</td>
                    <td>
                        <button class="view-btn" onclick="viewFullText(${item.id})">
                            👁️ View
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
        
        // Update pagination info
        document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages}`;
        document.getElementById('prevBtn').disabled = currentPage === 1;
        document.getElementById('nextBtn').disabled = currentPage === totalPages;
    }

    // Pagination functions
    window.previousPage = function() {
        if (currentPage > 1) {
            currentPage--;
            renderHistory();
        }
    }

    window.nextPage = function() {
        const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderHistory();
        }
    }

    // View full text in modal
    window.viewFullText = async function(id) {
        try {
            const response = await fetch(`/api/prediction/${id}`);
            const data = await response.json();
            
            const modal = document.getElementById('textModal');
            const modalText = document.getElementById('modalText');
            const modalPrediction = document.getElementById('modalPrediction');
            
            modalText.textContent = data.text;
            modalPrediction.textContent = data.prediction;
            modalPrediction.className = `modal-prediction-badge badge-${data.prediction.toLowerCase()}`;
            
            modal.style.display = 'flex';
        } catch (error) {
            console.error('Error loading full text:', error);
            alert('Failed to load full text');
        }
    }

    // Close modal
    window.closeModal = function() {
        document.getElementById('textModal').style.display = 'none';
    }

    // Clear all history with confirmation
    window.clearAllHistory = async function() {
        if (!confirm('Are you sure you want to clear ALL prediction history? This action cannot be undone!')) {
            return;
        }
        
        try {
            const response = await fetch('/api/clear-history', {
                method: 'POST'
            });
            
            if (response.ok) {
                alert('History cleared successfully!');
                loadStatistics();
                loadHistory();
            } else {
                alert('Failed to clear history');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            alert('Error clearing history');
        }
    }

    // Load dashboard data initially
    loadStatistics();
    loadHistory();
    
    // Refresh dashboard every 30 seconds
    setInterval(() => {
        loadStatistics();
        loadHistory();
    }, 30000);
    
    // Initialize image upload functionality
    initializeImageUpload();
});

// Export all data function (global scope for button onclick)
async function exportAllData() {
    window.location.href = '/api/export-all';
}

// Export all data to PDF function (global scope for button onclick)
async function exportAllDataPDF() {
    window.location.href = '/api/export-all-pdf';
}

// ========================================
// IMAGE ANALYSIS FUNCTIONS
// ========================================

// Current uploaded image
let currentImageFile = null;

// Switch between text and image analysis modes
function switchMode(mode) {
    const textSection = document.getElementById('textAnalysisSection');
    const imageSection = document.getElementById('imageAnalysisSection');
    const textModeBtn = document.getElementById('textModeBtn');
    const imageModeBtn = document.getElementById('imageModeBtn');
    const resultSection = document.getElementById('resultSection');
    
    if (mode === 'text') {
        textSection.style.display = 'block';
        imageSection.style.display = 'none';
        textModeBtn.classList.add('active');
        imageModeBtn.classList.remove('active');
    } else {
        textSection.style.display = 'none';
        imageSection.style.display = 'block';
        textModeBtn.classList.remove('active');
        imageModeBtn.classList.add('active');
    }
    resultSection.style.display = 'none';
}

// Initialize image upload functionality
function initializeImageUpload() {
    const uploadArea = document.getElementById('imageUploadArea');
    const fileInput = document.getElementById('imageFileInput');
    const previewSection = document.getElementById('imagePreviewSection');
    const imagePreview = document.getElementById('imagePreview');
    
    // Click to upload
    uploadArea.addEventListener('click', (e) => {
        if (e.target === uploadArea || e.target.closest('.upload-icon, h4, p')) {
            fileInput.click();
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleImageFile(file);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleImageFile(file);
        } else {
            alert('Please upload an image file (JPG, PNG, etc.)');
        }
    });
}

// Handle image file upload
function handleImageFile(file) {
    // Check file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        alert('Image size must be less than 10MB');
        return;
    }
    
    // Check file type
    if (!file.type.startsWith('image/')) {
        alert('Please upload a valid image file');
        return;
    }
    
    currentImageFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const imagePreview = document.getElementById('imagePreview');
        const uploadArea = document.getElementById('imageUploadArea');
        const previewSection = document.getElementById('imagePreviewSection');
        const resultsDiv = document.getElementById('imageAnalysisResults');
        
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        resultsDiv.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

// Remove uploaded image
function removeImage() {
    currentImageFile = null;
    document.getElementById('imageUploadArea').style.display = 'block';
    document.getElementById('imagePreviewSection').style.display = 'none';
    document.getElementById('imageAnalysisResults').style.display = 'none';
    document.getElementById('imageFileInput').value = '';
}

// Analyze image
async function analyzeImage(analysisType) {
    if (!currentImageFile) {
        alert('Please upload an image first');
        return;
    }
    
    const resultsDiv = document.getElementById('imageAnalysisResults');
    const resultsContent = document.getElementById('imageResultsContent');
    
    // Show loading
    resultsDiv.style.display = 'block';
    resultsContent.innerHTML = `
        <div class="image-analyzing">
            <div class="spinner"></div>
            <p>Analyzing image... This may take a moment.</p>
        </div>
    `;
    
    try {
        const formData = new FormData();
        formData.append('image', currentImageFile);
        formData.append('analysis_type', analysisType);
        
        const response = await fetch('/api/analyze-image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayImageAnalysisResults(data, analysisType);
        } else {
            resultsContent.innerHTML = `
                <div class="tampering-alert danger">
                    <h5>❌ Analysis Failed</h5>
                    <p>${data.error || 'An error occurred during analysis'}</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error analyzing image:', error);
        resultsContent.innerHTML = `
            <div class="tampering-alert danger">
                <h5>❌ Error</h5>
                <p>Failed to analyze image. Please try again.</p>
            </div>
        `;
    }
}

// Display image analysis results
function displayImageAnalysisResults(data, analysisType) {
    const resultsContent = document.getElementById('imageResultsContent');
    let html = '';
    
    // Visual Content Analysis (FAKE/REAL Prediction) - ONLY THIS NOW
    if (data.visual_analysis) {
        const va = data.visual_analysis;
        const isFake = va.prediction === 'FAKE';
        const isSuspicious = va.prediction === 'SUSPICIOUS';
        const badgeClass = isFake ? 'fake' : (isSuspicious ? 'warning' : 'real');
        const icon = isFake ? '❌' : (isSuspicious ? '⚠️' : '✅');
        
        html += `
            <div class="result-badge ${badgeClass}" style="margin-bottom: 1.5rem;">
                ${icon} ${va.prediction}
            </div>
            <div class="metadata-section" style="margin-bottom: 1.5rem;">
                <h5>🔍 Visual Content Analysis</h5>
                <div class="metadata-item">
                    <span class="metadata-label">Prediction:</span>
                    <span class="metadata-value">${va.prediction}</span>
                </div>
                <div class="metadata-item">
                    <span class="metadata-label">Confidence:</span>
                    <span class="metadata-value">${va.confidence}</span>
                </div>
                <div class="metadata-item">
                    <span class="metadata-label">Analysis:</span>
                    <span class="metadata-value">${va.message}</span>
                </div>
        `;
        
        // Show indicators if any
        if (va.indicators && va.indicators.length > 0) {
            html += `
                <div style="margin-top: 0.75rem;">
                    <strong>Indicators Found:</strong>
                    <ul style="margin-left: 1.5rem; margin-top: 0.5rem; color: #64748b;">
            `;
            va.indicators.forEach(indicator => {
                html += `<li>${indicator}</li>`;
            });
            html += `</ul></div>`;
        }
        
        html += `</div>`;
    }
    
    resultsContent.innerHTML = html;
}

