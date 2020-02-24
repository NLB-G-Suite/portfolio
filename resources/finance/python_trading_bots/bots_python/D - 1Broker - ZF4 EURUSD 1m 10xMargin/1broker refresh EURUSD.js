/*
** AmiBroker/Win32 scripting Example
**
** File:	 ASX.js
** Created:	 Tomasz Janeczko, January 12th, 2000
** Purpose:	 Download and import quotes from www.australian-stockmarket.com
** Language: 	 JavaScript (Windows Scripting Host)
**
**
*/

/**************************************************************/
/* Constants                                                  */
/**************************************************************/

/* The ticker to check */
ChkTicker = "XAO";

/* The folder where the files will be downloaded */
DestDir = "C:\\ASX\\";

/* The name and the path to downloader program */
DownloaderPrg  = "URLGet.exe";

/* Force download - if true causes downloading data file */
/* even if it exists on the local drive */  
ForceDownloadFlag = false;

/* URL from where data are downloaded */
/* Note that australian-stockmarket site changed directory for 2001 quotes */
URLPrefix = "http://www.australian-stockmarket.com/updates/";
URLPrefix2001 = "http://www.australian-stockmarket.com/updates2001/";

/* extension of file name, YYYYMMDD will be prepended */
FileExt = ".prn";

/* max number of days to download when history is empty */
nMaxHistoryLen = 365;

/**************************************************************/
/* Main part                                                  */
/**************************************************************/

/* Create AmiBroker app object */
AmiBroker = new ActiveXObject( "Broker.Application" );
/* ... and file system object */
FileSys = new ActiveXObject( "Scripting.FileSystemObject" );
WshShell = new ActiveXObject( "WScript.Shell" );

var MiliSecInDay = 24 * 60 * 60 * 1000;

function Download( URL, filename )
{
	if( ! ForceDownloadFlag && FileSys.FileExists( filename ) ) return true;

	if( WshShell.Run( DownloaderPrg + " " + URL + " " + filename, 0, true ) == 0 ) return true;

	WScript.echo("Download of " + URL + " failed." );

	return false;
}

function Import( filename )
{
	try
	{
		AmiBroker.Import( 0, filename, "custom99.format" );
	}
	catch( e )
	{
		return false;
	}

	/* refresh ticker list and windows */
	AmiBroker.RefreshAll();
	return true;
}

function CheckFolder()
{
	if( ! FileSys.FolderExists( DestDir ) )
	{
		FileSys.CreateFolder( DestDir );
	}
}

function GetNumberOfDaysToLoad()
{
	var Today = new Date();
	var LastDate = new Date();

	LastDate.setDate( LastDate.getDate() - nMaxHistoryLen ); // one year

	if( AmiBroker.Stocks.Count > 0 )
	{
		nQty = AmiBroker.Stocks( ChkTicker ).Quotations.Count;
		if( nQty > 0 )
		{
			LastDate = new Date( AmiBroker.Stocks( ChkTicker ).Quotations( nQty - 1 ).Date );
		}
	}


	// the difference is in milliseconds	
	return ( Math.floor( (Today - LastDate)/MiliSecInDay ) );

}

function IsValidDatabase()
{
	if( AmiBroker.Stocks.Count > 0 )
	{
		try
		{
			return AmiBroker.Stocks( ChkTicker ).Ticker == ChkTicker;
		}
		catch( e )
		{
			WScript.echo("The database currently loaded into AmiBroker does not have " + ChkTicker + "\nSo I guess this is not correct database.\nUpdate failed.");
		}
	}

	return false;
}

function Main()
{
	bOK = true;
/*
	if( ! IsValidDatabase() ) return;
	
	var CurDate = new Date();
	var NumDays = GetNumberOfDaysToLoad();

	WScript.echo("Your database is " + NumDays + " day(s) old.\n" + (NumDays > 0 ? "Downloading missing quotes" : "No update is needed" ) );

	CheckFolder();

	**#for( i = 0; i < NumDays; i++ )
	**#{
	**#	if( CurDate.getDay() > 0 && CurDate.getDay() < 6 )
	**#	{
	**#		// bussiness day
	**#		y = CurDate.getFullYear();
	**#		m = CurDate.getMonth() + 1;
	**#		d = CurDate.getDate();
    **#
	**#		bOK = true;
    **#
	**#		filename = y + ( m < 10 ? "0" : "" ) + m + ( d < 10 ? "0" : "" ) + d + FileExt;
    **#
	**#		URL = URLPrefix + filename;
    **#
	**#		if( y == 2001 && URLPrefix2001 != "" )
	**#		{
	**#			URL = URLPrefix2001 + filename;
	**#		}
    **#
	**#		if( Download( URL, DestDir + filename ) )
	**#		{
	**#			if( ! Import( DestDir + filename ) ) bOK = false;
	**#		}
	**#		else
	**#		{
	**#			bOK = false;
	**#		}
    **#
	**#		if( ! bOK && WshShell.popup( "The download and/or import of the " + filename + " has failed.\nThis can be because the data are not available or network connection problem.\nDo you want to abort?" , 0, "Abort updating", 4 + 256 ) == 6 )
	**#		{ 
	**#			break;
	**#		}
    **#
	**#	}
    **#
	**#	CurDate.setDate( CurDate.getDate() - 1 );
	**#}
*/	
	Import("F:\\Cripto\\Cryptotrader\\AMIBROKER\\EURUSD_1broker.csv")
	
    //if( bOK )  WScript.echo("Update script finished. Your database is now up-to-date" );
    //else       WScript.echo("Update script finished. There were, however, some errors during download/import");

}

Main();

