<?php
$file = "./dialog_act_data4.txt";
$filev = "./vectors.txt";
$neg = "./neg-words.txt";
$pos = "./pos-words.txt";

function get_words($s) {
 	$s = preg_replace('/([a-zA-z0-9])([[:punct:]])/','$1 $2',$s); 
	$words = preg_split('/[\s,]+/',$s);  
	return $words;
}

function contains_question($sentence) {
	$pattern = "/(^|[\s]|[[:punct:]])(who|what|where|when|why|how|which)([[:punct:]]|[\s]|$)/";
	$pattern2 = "/\?/";
	preg_match($pattern, $sentence, $matches);
	preg_match($pattern2, $sentence, $matches2);
	if(count($matches)>0||count($matches2)>0) return true;
	else return false;
}

function contains_yes($sentence) {
	$pattern = "/(^|[\s]|[[:punct:]])(yes|yeah|yup|yep|right|agree|ya|ok|okay|true|sure)([[:punct:]]|[\s]|$)/";
	$filter = "/\?/";
	preg_match($pattern, $sentence, $matches);
	preg_match($filter, $sentence, $matches2);
	
	if(count($matches)>0&&count($matches2)==0) return true;
	else return false;
}

function contains_no($sentence) {
	$pattern = "/(^|[\s]|[[:punct:]])(no|nope|nah|newp|not|dont|don't|nu)([[:punct:]]|[\s]|$)/";
	$filter = "/\?/";
	preg_match($pattern, $sentence, $matches);
	preg_match($filter, $sentence, $matches2);
	if(count($matches)>0&&count($matches2)==0) return true;
	else return false;
}

function contains_bye($sentence) {
	$pattern = "/(^|[\s]|[[:punct:]])(brb|bye|see\s(ya|you)|afk|bbl|bbs|tc|hb|byes|cheers|cya|nite|night)([[:punct:]]|[\s]|$)/";
	preg_match($pattern, $sentence, $matches);
	if(count($matches)>0) return true;
	else return false;
}

function contains_sign($sentence) {
	$pattern = "/(:|;|!|lol|haha|hehe|omg|lmao)/";
	preg_match($pattern, $sentence, $matches);
	if(count($matches)>0) return true;
	else return false;
}

function dialog_act_features($original,$class) {
 	$fv = array();
 	if(contains_question($original))$fv["contains_question"] = true;
 	if(contains_yes($original))$fv["contains_yes"] = true;
 	if(contains_no($original))$fv["contains_no"] = true;
 	if(contains_bye($original))$fv["contains_bye"] = true;
 	if(contains_sign($original))$fv["contains_sign"] = true;
 	$original = get_words($original);
 		
 	foreach($original as $k=>$v) {

 		if($k-1>-1) $previous = $original[$k-1];
 		else $previous = "<START>";
 		if($k+1<count($original)) $next = $original[$k+1]; 
 		else $next = "<END>"; 
 		
 		$fv["$v"] = true;
 		$fv["$previous $v"] = true;
 	}
 	
 	$fv["<y>"] = $class;
 	return $fv;
 }
  
function train_naive_bayes($fv) {
 	$tot = array();
 	$i = 0;
 	$N = count($fv);
 	$R = array();
 	foreach($fv as $f) {
 		if(isset($tot[$f["<y>"]]))$tot[$f["<y>"]]++;
 		else $tot[$f["<y>"]] = 1;
 	}
 	
 	foreach($fv as $k=>$f) {
 		$i++;
 		print("Training $i/$N\r");
 		foreach($f as $fn=>$e) {
 			if($fn != "<y>") {
 				if(isset($R[$fn][$f["<y>"]])) $R[$fn][$f["<y>"]] += 1/($tot[$f["<y>"]]+2);
				else $R[$fn][$f["<y>"]] = 2/($tot[$f["<y>"]]+2);
 			}
 		}
 	}
 	
 	foreach($tot as $k=>$v) {
 		$R['<DEFAULT>'][$k] = 2/($N+2);
 		$tot[$k] /= $N;
 	}
 	$R['<CLASSES>'] = $tot;
 	return $R;
 }

function classify_naive_bayes($model,$fv) {
 	$p = array();
 	// pr(X) = pr(X1).pr(X2).pr(X3) ==> log(pr(X)) = log(pr(X1)) + log(pr(X2)) + log(pr(X3))
 	
 	foreach($model["<CLASSES>"] as $class=>$c) {
 		$p[$class] = log($model["<CLASSES>"][$class]);
 		foreach ($fv as $fn=>$f) {
 			if($fn != "<y>") {
 					if(isset($model[$fn][$class])) $p[$class] += log($model[$fn][$class]);
					else $p[$class] += log($model["<DEFAULT>"][$class]);
 				}
 		}
 	}
 	//print_r($p);
 	$max = -1000000;
 	$winner = "";
 	foreach($p as $k=>$v) {
 		if($v>$max) {
 			$max = $v;
 			$winner = $k;
 		}
 	}
 	return array('winner'=>$winner,'p'=>$p);
 }
 
function evaluate_naive_bayes($model,$sentences) {
	$p = array();
	$pr = array();
	foreach($model["<CLASSES>"] as $k=>$v) {
		foreach($model["<CLASSES>"] as $k1=>$v1) {
			$p[$k][$k1] = 0;
		}	
	}
	foreach ($sentences as $s) {
		$fv1 = dialog_act_features($s[0],$s[1]);
		$p[$s[1]][classify_naive_bayes($model,$fv1)["winner"]]++;
 	}
 	$all = 0;
 	$hits = 0;
 	foreach($p as $k=>$v) {
 		$tmp = 0;
 		foreach($p as $k1=>$v1) {
 			$tmp += $p[$k][$k1];
 		}
 		$pr[$k] = $p[$k][$k]/$tmp;
 		$all += $tmp;
 		$hits += $p[$k][$k];
 	}
 	$pr['<PRECISION>'] = 100*$hits/$all;
 	//print_r($p);
 	//print_r($pr);
 	return $pr;
}

function dot_product($v1, $v2) {
	
	if(count($v1) == 0 && count($v2) == 0) return 0;
	if(count($v1) == 0 || count($v2) == 0) return 0;
	if(count($v1) != count($v2)) return -1;
	$tmp = 0;
	for($i=0; $i<count($v1); $i++) {
		$tmp += ($v1[$i])*($v2[$i]);
	}
	return $tmp;
}

function get_wordvect($sentence,$wvectors,$separator) {
	$a1 = explode($separator,trim($sentence));
	$tmp1 = array();
	foreach($a1 as $term) {
		if(isset($wvectors[$term])) $tmp1[] = $wvectors[$term];
	}
	return get_centroid($tmp1);
}

function get_centroid($vs) {
	$n = count($vs);
	if($n<1) return -1;
	$tmp = array();
	foreach($vs as $v) {
		if(is_array($v)){
			for($i=0; $i<count($v); $i++) {
				$a = $v[$i]/$n;
				if(isset($tmp[$i]))$tmp[$i] += $a;
				else $tmp[] = $a;
			}
		}
	}
	return $tmp;
}

function semantic_similarity_dot($sentence1, $sentence2, $separator1, $separator2, $wvectors) {
	$tmp1 = get_wordvect($sentence1,$wvectors,$separator1);
	$tmp2 = get_wordvect($sentence2,$wvectors,$separator2);
	return round(dot_product($tmp1, $tmp2),2);
}

function load_word_vectors($fname) {
	$vectors = array();
	$handle = fopen($fname, "r");
	$raw = fread($handle,filesize($fname));
	fclose($handle);
	$tb = explode("\n",$raw);
	foreach ($tb as $rt) {
		$n = explode(" ",$rt);
		$vectors[$n[0]] = array_slice($n,1);
	}
	return $vectors;
}

function positive_score($pos, $sentence, $wvectors) {
	$training = array();
	$handle = fopen($pos, "r");
	$raw = fread($handle,filesize($pos));
	fclose($handle);
	return semantic_similarity_dot($raw,$sentence,"\n"," ",$wvectors);
}

function negative_score($neg, $sentence, $wvectors) {
	$training = array();
	$handle = fopen($neg, "r");
	$raw = fread($handle,filesize($neg));
	fclose($handle);
	return semantic_similarity_dot($raw,$sentence,"\n"," ",$wvectors);
}

function knn_classify_sentiment($pos,$neg,$word,$wvectors,$k) {
	$distances = array();
	$handle = fopen($pos, "r");
	$raw = fread($handle,filesize($pos));
	fclose($handle);
	$terms = explode("\n",$raw);
	$pscore = 0;
	$nscore = 0;
	foreach ($terms as $term) {
		$distances[] = array('score'=>semantic_similarity_dot($term,$word,"\n"," ",$wvectors),'class'=>"pos");
	}
	$handle = fopen($neg, "r");
	$raw = fread($handle,filesize($neg));
	fclose($handle);
	$terms = explode("\n",$raw);
	foreach ($terms as $term) {
		$distances[] = array('score'=>semantic_similarity_dot($term,$word,"\n"," ",$wvectors),'class'=>"neg");
	}
	rsort($distances);
	//print_r($distances);
	for($n = 0; $n < $k; $n++) {
		if($distances[$n]['class'] == "pos") $pscore++;
		else $nscore++;
	}
	
	return array('pos'=>$pscore,'neg'=>$nscore);
}

//****************//
$wvectors = array();
$wvectors = load_word_vectors($filev);

$sentence = "like";
$sentence = "hate";

$sentence = "friendly";
$sentence = "hostile";

$sentence = "love";
$sentence = "detest";

$sentence = "beautiful";
$sentence = "horrible";

$sentence = "amusing";
$sentence = "noisy";

$neg_score = negative_score($neg, $sentence, $wvectors);
$pos_score = positive_score($pos, $sentence, $wvectors);
echo "pscore = $pos_score \nnscore = $neg_score\n\n";











exit;






$knnrez = knn_classify_sentiment($pos,$neg,$sentence,$wvectors,3);
$pscore = $knnrez['pos'];
$nscore = $knnrez['neg'];
echo "pscore = $pscore \nnscore = $nscore\n\n";










exit;
$neg_score = negative_score($neg, $sentence, $wvectors);
$pos_score = positive_score($pos, $sentence, $wvectors);
echo "pscore = $pos_score \nnscore = $neg_score\n\n";














exit;

$sentence = "bad restaurant bad experience";
//$sentence = "I did not like the food and the service was slow and bad";


$fv = array();
$fv1 = dialog_act_features("Hi there","Greeting");
$fv[] = $fv1;
$fv1 = dialog_act_features("Hello there","Greeting");
$fv[] = $fv1;
$fv1 = dialog_act_features("Hello my friend","Greeting");
$fv[] = $fv1;
$fv1 = dialog_act_features("I like pizza","Statement");
$fv[] = $fv1;
$fv1 = dialog_act_features("I love pizza","Statement");
$fv[] = $fv1;
$fv1 = dialog_act_features("I like you","Statement");
$fv[] = $fv1;

$M = train_naive_bayes($fv);
print_r($M);




$fv1 = dialog_act_features("I love you friend","");
$fv2 = dialog_act_features("Hello you","");
print_r(classify_naive_bayes($M,$fv1));
print_r(classify_naive_bayes($M,$fv2));
exit;

$fvt = dialog_act_features("I have to go now, bye","Bye");
print_r($fvt);
exit;


$handle = fopen($file,"r");
if($handle<0) {echo "error opening file"; return -1;}
$raw = fread($handle,filesize($file));
fclose($handle);
$sraw = explode("\n",$raw);
$fv = array();
$i = 0;
$N = count($sraw);
$sentences = array();

$ftmp = array();
foreach($sraw as $r) {
	$s = explode(" +++ ",$r);
	if(count($s)>1) {
		$fv1 = dialog_act_features($s[0],$s[1]);
		$i++;
		print("Extracting features $i/$N\r");
		
		if($i<4000)$fv[] = $fv1;
		else {
			$sentences[] = $s;
		}
	}
}

$M = train_naive_bayes($fv);
print_r(evaluate_naive_bayes($M,$sentences));

?>